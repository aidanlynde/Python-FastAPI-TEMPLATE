# fastapi
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# firebase and models
from firebase_admin import firestore, auth as firebase_auth
import firebase_admin
from firebase_admin import credentials

# other imports
from typing import Generator
from .schemas import TokenData

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

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        print(f"Received token: {token}")  # Debugging line
        decoded_token = firebase_auth.verify_id_token(token)
        print(f"Decoded token: {decoded_token}")  # Debugging line
        email = decoded_token.get("email")
        uid = decoded_token.get("uid")
        if email is None or uid is None:
            print("Email or UID not found in token")  # Debugging line
            raise credentials_exception
        print(f"Token email: {email}, UID: {uid}")  # Debugging line
        return TokenData(email=email, uid=uid)
    except Exception as e:
        print(f"Error verifying token: {e}")  # Debugging line
        raise credentials_exception
