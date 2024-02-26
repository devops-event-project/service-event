from fastapi import FastAPI
from routes.event import event

app = FastAPI()

app.include_router(event)