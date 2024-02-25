from fastapi import FastAPI
from .api.router import api_router

app = FastAPI(title="My FastAPI Project")

app.include_router(api_router)

@app.get("/")
async def read_root():
    return {"Hello": "World"}