from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def read_activity():
    return {"Activity": "Welcome to Slush"}
