from fastapi import FastAPI

app = FastAPI()

# Initialize firebase 
import firebase_admin
from firebase_admin import credentials

@app.on_event("startup")
def startup_event():
    cred = credentials.Certificate("/Users/kareembenaissa/dev/python_dev/slushbrain/slushchat-oaruvo-firebase-adminsdk-7ez3i-399bc3252c.json")
    firebase_admin.initialize_app(cred, {
        'projectId': 'slushchat-oaruvo',
    })

# Import routers after Firebase initialization
from .api.router import api_router

app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

