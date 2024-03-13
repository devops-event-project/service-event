from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.event import event


service_event = FastAPI()

service_event.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://0.0.0.0:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service_event.include_router(event)





# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from routes.userRoutes import user
#
# service_user = FastAPI()
#
# service_user.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000", "http://0.0.0.0:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
#
# service_user.include_router(user)
