# fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# firebase and models
from firebase_admin import firestore, auth as firebase_auth
import firebase_admin
from firebase_admin import credentials

# other imports
from typing import Generator

# Initialize Firebase Admin in your main.py or here with a check to prevent reinitialization
def get_firebase_app():
    if not firebase_admin._apps:
        cred = credentials.Certificate("secrets/fbsa_creds.json")
        firebase_admin.initialize_app(cred, {
            'projectId': 'urbanag-9f106',
        })
    return firebase_admin.get_app()

def get_firestore_client() -> firestore.firestore.Client:
    app = get_firebase_app()  # Ensure Firebase is initialized
    return firestore.client(app=app)


# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_token = firebase_auth.verify_id_token(token)
        email = decoded_token.get("email")
        if email is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    return decoded_token  # You can return the entire decoded token or just the email