import datetime

from bson import ObjectId
from fastapi import APIRouter
from config.db import conn
from models.event import Event, Attendee, Reminder
from schemas.event import serializeDict, serializeList
from notification.notification import NotificationService

event = APIRouter(prefix='/event')

notification_service = NotificationService()

@event.get('/', tags=["Get Methods"])
async def find_all_events():
    return serializeList(conn.local.event.find())

@event.get('/{id}', tags=["Get Methods"])
async def fine_one_event(id: str):
    return serializeDict(conn.local.event.find_one({"_id":ObjectId(id)}))

@event.post('/')
@event.post('/event/', tags=["Post Methods"])
async def create_event(event: Event):
    event_params = dict(event)

    reminders_dict = list(map(dict, event_params['reminders']))
    attendees_dict = list(map(dict, event_params['attendees']))

    event_params['reminders'] = reminders_dict
    event_params['attendees'] = attendees_dict

    result = conn.local.event.insert_one(event_params)

    reminder_time = event_params['startDateTime']
    time_change = datetime.timedelta(minutes=event_params['reminders'][0]['timeBefore'])
    reminder_time = reminder_time - time_change
    string_time = reminder_time.strftime('%Y-%m-%dT%H:%M:%S')

    email_params = {
        'email': 'milankopp2@gmail.com', #TODO: get user email address from cookies
        'subject': 'Event Reminder',
        'body': f'You have an event in {event_params["reminders"][0]["timeBefore"]} minutes. '
                f'Title: {event_params["title"]}, '
                f'Description: {event_params["description"]}, '
                f'Location: {event_params["location"]}',
        'time': string_time
    }


    notification_service.schedule_email(email_params)
    return serializeDict(conn.local.event.find_one({"_id":result.inserted_id}))

@event.put('/{id}', tags=["Put Methods"])
async def update_event(id: str, event: Event):
    update_result = conn.local.event.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(event)}
    )
    if update_result is None:
        return {"error": "Event not found"}
    return serializeDict(conn.local.event.find_one({"_id": ObjectId(id)}))

@event.delete('/{id}', tags=["Delete Methods"])
async def delete_event(id: str):
    return serializeDict(conn.local.event.find_one_and_delete({"_id":ObjectId(id)}))
