from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from firebase_admin import credentials, auth as firebase_auth, firestore
import firebase_admin
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_current_user, get_firebase_app, get_firestore_client
from .models import UserProfile

app = FastAPI()

# Initialize firebase 
@app.on_event("startup")
def startup_event():
    cred = credentials.Certificate("secrets/fbsa_creds.json")
    try:
        firebase_admin.initialize_app(cred, {
            'projectId': 'urbanag-9f106',
        })
    except Exception as e:
        print(f"Error initializing Firebase: {e}")


# CORS middleware
origins = [
    "http://localhost:3000",
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/users/me", response_model=dict)
def read_users_me(current_user: dict = Depends(get_current_user), db=Depends(get_firestore_client)):
    print(f"Current user: {current_user}")  # Debugging line
    email = current_user.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user_doc = db.collection('users').document(email).get()
    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")
    return user_doc.to_dict()


@app.get("/api/data")
async def get_data():
    return {"message": "Hello from FastAPI"}


@app.post("/save_profile")
async def save_profile(user_profile: UserProfile, db=Depends(get_firestore_client)):
    try:
        user_ref = db.collection('users').document(user_profile.uid)
        user_ref.set({
            'full_name': user_profile.full_name,
            'age': user_profile.age,
            'gender': user_profile.gender,
            'height': user_profile.height,
            'weight': user_profile.weight,
            'email': user_profile.email
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}

