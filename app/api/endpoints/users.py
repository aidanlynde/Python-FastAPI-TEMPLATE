#fastapi
from fastapi import APIRouter, Depends

#dependencies and models
from ...dependencies import get_users, get_user

from ...models import User

router = APIRouter()

@router.get("/")
async def read_users(users: list = Depends(get_users)):
    return {"Users": users}

@router.get("/{user_id}", response_model=User)
async def read_user(user: User = Depends(get_user)):
    return user

# @router.get("/")
# async def read_users(db: firestore.firestore.Client = Depends(get_firestore_client)):
#     users_ref = db.collection('users')
#     users = users_ref.stream()
#     users_list = [user.to_dict() for user in users]
#     return {"Users": users_list}


# @router.get("/")
# async def read_users():
#     users_ref = db.collection('users')
#     users = users_ref.stream()
#     users_list = get_users()
#     return {"Users": users_list}



