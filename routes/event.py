import datetime
import json
from bson import ObjectId
from fastapi import APIRouter, Depends

# Importing local modules
from config.db import events
from models.event import Event, Attendee, Reminder
from schemas.event import serializeDict, serializeList
from notification.notification import NotificationService
from event_store.event_store import KAFKA_TOPIC, publish_event, consume_events
from security.auth import get_current_user

"""
This module integrates FastAPI with MongoDB, Kafka, and AWS for event management,
including creating, updating, and deleting events.
The API routes offer functionalities:
listing all events for a user,
finding a specific event,
publishing and consuming event to event store,
managing event reminders and attendee notifications via scheduled emails.
"""

# Creating APIRouter
event = APIRouter(prefix='/event')

# Initializing the notification service
notification_service = NotificationService()

# Route to get all events for the current user
@event.get('/', tags=["Get Methods"])
async def find_all_events(current_user: dict = Depends(get_current_user)):
    username = current_user['username']
    return serializeList(events.find({"userID": username}))

# Route to get a single event by ID
@event.get('/{id}', tags=["Get Methods"])
async def fine_one_event(id: str):
    return serializeDict(events.find_one({"_id":ObjectId(id)}))

# Route to consume logs from the event store
@event.get("/consume-logs/")
async def consume_logs(max_messages: int = 5):
    messages = consume_events(max_messages=max_messages)
    decoded_messages = [message.decode('utf-8') for message in messages]
    return {"messages": messages}

# Route to create a new event
@event.post('/create', tags=["Post Methods"])
async def create_event(event: Event):
    event_params = dict(event)

    reminders_dict = list(map(dict, event_params['reminders']))
    attendees_dict = list(map(dict, event_params['attendees']))

    event_params['reminders'] = reminders_dict
    event_params['attendees'] = attendees_dict

    # publish events to event store
    publish_event("post","sample")

    # Handling reminders and scheduling notifications
    reminder_time = event_params['startDateTime']
    time_change = datetime.timedelta(minutes=event_params['reminders'][0]['timeBefore'])
    reminder_time = reminder_time - time_change
    string_time = reminder_time.strftime('%Y-%m-%dT%H:%M:%S')

    # Adding current user to all attendees
    all_attendees = attendees_dict
    all_attendees.append({"userID": event_params["userID"], "attending": "True"})

    # Creating an event for each attendee and scheduling email notifications
    for attendee in all_attendees:
        event_params["userID"] = attendee["userID"]
        result = events.insert_one(event_params)
        del event_params['_id']

        # Scheduling email notification for the event
        email_params = {
            'email': attendee["userID"],
            'subject': 'Event Reminder',
            'body': f'You have an event in {event_params["reminders"][0]["timeBefore"]} minutes. '
                    f'Title: {event_params["title"]}, '
                    f'Description: {event_params["description"]}, '
                    f'Location: {event_params["location"]}',
            'time': string_time
        }
        notification_service.schedule_email(email_params)

    return serializeDict(events.find_one({"_id":result.inserted_id}))

# Route to update an existing event
@event.put('/{id}', tags=["Put Methods"])
async def update_event(id: str, event: Event):
    update_result = events.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(event)}
    )
    if update_result is None:
        return {"error": "Event not found"}
    # publish events to event store
    # publish_event("put",dict(event))
    return serializeDict(events.find_one({"_id": ObjectId(id)}))

# Route to delete an event
@event.delete('/{id}', tags=["Delete Methods"])
async def delete_event(id: str):
    # publish events to event store
    # publish_event("delete",{"id": id})
    return serializeDict(events.find_one_and_delete({"_id":ObjectId(id)}))
