from bson import ObjectId
from fastapi import APIRouter
from config.db import conn
from models.event import Event
from schemas.event import serializeDict, serializeList

event = APIRouter(prefix='/event')

@event.get('/', tags=["Get Methods"])
async def find_all_events():
    return serializeList(conn.local.event.find())

@event.get('/{id}', tags=["Get Methods"])
async def fine_one_event(id: str):
    return serializeDict(conn.local.event.find_one({"_id":ObjectId(id)}))

@event.post('/')
@event.post('/event/', tags=["Post Methods"])
async def create_event(event: Event):
    result = conn.local.event.insert_one(dict(event))
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
