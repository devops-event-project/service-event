from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    title: str
    description: str
    start: datetime
    end: datetime
    location: str
    reminder_type: str
    reminder_time: int