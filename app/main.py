from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import credentials, auth as firebase_auth, firestore
import firebase_admin

from .dependencies import get_current_user, get_firebase_app, get_firestore_client

app = FastAPI()

# Initialize firebase 
import firebase_admin
from firebase_admin import credentials

@app.on_event("startup")
def startup_event():
    cred = credentials.Certificate("secrets/fbsa_creds.json")
    try:
        firebase_admin.initialize_app(cred, {
            'projectId': 'urbanag-9f106',
        })
    except Exception as e:
        print(f"Error initializing Firebase: {e}")


# Import routers after Firebase initialization
from .api.router import api_router


@app.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = firebase_auth.get_user_by_email(form_data.username)
        custom_token = firebase_auth.create_custom_token(user.uid)
        return {"access_token": custom_token, "token_type": "bearer"}
    except firebase_auth.UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        print(f"Error in /token endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )

""" @app.get("/users/me", response_model=dict)
def read_users_me(current_user: dict = Depends(get_current_user), db=Depends(get_firestore_client)):
    # Example of querying Firestore
    user_doc = db.collection('users').document(current_user['email']).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return user_doc.to_dict() """


app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

