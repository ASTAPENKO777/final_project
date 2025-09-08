from fastapi import FastAPI
from models import Base
from schemas.user import UserCreate

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}