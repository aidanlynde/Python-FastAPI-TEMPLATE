from .schemas import UserCreate, UserResponse
from firebase_admin import firestore
from fastapi import HTTPException

# CRUD operations
#  These functions are responsible for interacting with the Firestore database
#  They are designed to be used by the API endpoints in the FastAPI application. 

# Notes: 
#   - The `db` parameter is a Firestore client instance, which is created by the `get_firestore_client` dependency. The functions defined in "endpoints/" use Depends, but the CRUD functions themselves do not.
#   - The `UserCreate` schema is used to validate the request body in the `create_user` function. This is a Pydantic schema that is defined in "schemas.py".

def create_user(db: firestore.firestore.Client, user_create: UserCreate) -> dict:
    # Convert Pydantic model to dict
    user_dict = user_create.dict()
    # Add a new document
    new_user_ref = db.collection('users').add(user_dict)
    # Return the created user data, potentially merging with the ID
    # I am merging with the ID here because I removed the ID from the UserCreate schema
    return {"id": new_user_ref[1].id, **user_dict}


def get_user(db: firestore.firestore.Client, user_id: str) -> UserResponse:
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    # I am merging with the ID here because I removed the ID from the UserResponse schema
    return UserResponse(uid=user_doc.id, **user_doc.to_dict())


# def get_users(db: firestore.firestore.Client) -> list:
#     users_ref = db.collection('users')
#     return [{"id": doc.id, **doc.to_dict()} for doc in users_ref.stream()]
# def update_user(db: firestore.firestore.Client, user_id: str, user_update: dict) -> dict:
#     user_ref = db.collection('users').document(user_id)
#     user_ref.update(user_update)
#     return get_user(db, user_id)  # Re-fetch the updated user