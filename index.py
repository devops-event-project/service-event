from fastapi import FastAPI
from routes.event import event


service_event = FastAPI()

service_event.include_router(event)