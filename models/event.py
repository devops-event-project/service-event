from pydantic import BaseModel
from datetime import datetime
from typing import List


class Reminder(BaseModel):
    type: str
    timeBefore: int

class Attendee(BaseModel):
    userID: str
    attending: str


class Event(BaseModel):
    userID: str
    title: str
    description: str
    startDateTime: datetime
    endDateTime: datetime
    location: str
    reminders: List[Reminder]
    attendees: List[Attendee]
