#fastapi
from fastapi import APIRouter, Depends

#firebase
from firebase_admin import firestore

#dependencies, schemas
#use schemas instead of models because the schemas represent the request and response data, while models represent the data in the database
#use crud to update database, and dependencies to connect to database.

from ...dependencies import get_firestore_client
from ...schemas import UserCreate, UserResponse
from ...crud import create_user, get_user

from typing import List

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: str, db: firestore.firestore.Client = Depends(get_firestore_client)):
    user = get_user(db, user_id)
    return user

@router.post("/users/", response_model=UserResponse)
def create_user_endpoint(user_create: UserCreate, db: firestore.firestore.Client = Depends(get_firestore_client)):
    return create_user(db, user_create)




