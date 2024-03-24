from pydantic import BaseModel
from datetime import datetime
from typing import List

# Creating Models for Reminder
class Reminder(BaseModel):
    type: str
    timeBefore: int

# Creating Models for Attendee
class Attendee(BaseModel):
    userID: str
    attending: str

# Creating Models for Event
class Event(BaseModel):
    userID: str
    title: str
    description: str
    startDateTime: datetime
    endDateTime: datetime
    location: str
    reminders: List[Reminder]
    attendees: List[Attendee]
