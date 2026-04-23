from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import bcrypt

app = FastAPI()

users_db = {}

class User(BaseModel):
    username: str
    password: str

def hash_password(password: str):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)


@app.get("/")
def root():
    return {"message": "Auth API running"}


@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed = hash_password(user.password)
    users_db[user.username] = hashed

    return {"message": "User registered successfully"}


@app.post("/login")
def login(user: User):
    if user.username not in users_db:
        raise HTTPException(status_code=400, detail="User not found")

    stored_password = users_db[user.username]

    if not verify_password(user.password, stored_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"message": "Login successful"}