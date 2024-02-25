from fastapi import APIRouter
from .endpoints import users, activity

# Create a new router for aggregating all endpoint routers
api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])