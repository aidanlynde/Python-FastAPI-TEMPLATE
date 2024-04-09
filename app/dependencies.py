#fastapi
# from fastapi import Depends, HTTPException

#typing
# from typing import List

#firebase and models
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

# from .schemas import UserResponse

# Initialize Firebase Admin in your main.py or here with a check to prevent reinitialization
def get_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate("secrets/fbsa_creds.json")
        firebase_admin.initialize_app(cred, {
            'projectId': 'slushchat-oaruvo',
        })
    return firebase_admin.get_app()

def get_firestore_client() -> firestore.firestore.Client:
    app = get_firebase_app()  # Ensure Firebase is initialized
    return firestore.client(app=app)
