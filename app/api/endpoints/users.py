from fastapi import APIRouter, Depends
from firebase_admin import firestore

from ...dependencies import get_firestore_client

router = APIRouter()

@router.get("/")
async def read_users(db: firestore.firestore.Client = Depends(get_firestore_client)):
    users_ref = db.collection('users')
    users = users_ref.stream()
    users_list = [user.to_dict() for user in users]
    return {"Users": users_list}

# @router.get("/")
# async def read_users():
#     users_ref = db.collection('users')
#     users = users_ref.stream()
#     users_list = get_users()
#     return {"Users": users_list}

