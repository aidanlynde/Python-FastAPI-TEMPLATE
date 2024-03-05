#fastapi
from fastapi import Depends, HTTPException

#firebase and models
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

from .models import User

# Initialize Firebase Admin in your main.py or here with a check to prevent reinitialization
def get_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate("/Users/kareembenaissa/dev/python_dev/slushbrain/slushchat-oaruvo-firebase-adminsdk-7ez3i-399bc3252c.json")
        firebase_admin.initialize_app(cred, {
            'projectId': 'slushchat-oaruvo',
        })
    return firebase_admin.get_app()

def get_firestore_client() -> firestore.firestore.Client:
    app = get_firebase_app()  # Ensure Firebase is initialized
    return firestore.client(app=app)





# Example dependency that fetches and yields users
def get_users(db: firestore.firestore.Client = Depends(get_firestore_client)):
    users_ref = db.collection('users')
    users = users_ref.stream()
    users_list = [user.to_dict() for user in users]
    return users_list

def get_user(user_id: str, db: firestore.firestore.Client = Depends(get_firestore_client)):
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        # Convert the Firestore document to a User model instance
        user_dict = user_doc.to_dict()
        return User(**user_dict)  # Unpack the dictionary into the User model
    else:
        raise HTTPException(status_code=404, detail="User not found")