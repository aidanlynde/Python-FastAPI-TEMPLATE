from fastapi import APIRouter
from .endpoints import users, activity, chatbot

# Create a new router for aggregating all endpoint routers
api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(chatbot.router, prefix="/api", tags=["chatbot"])