from fastapi import APIRouter, HTTPException, Depends
from jose import jwt
from passlib.context import CryptContext
from app.schemas import UserIn, UserOut
from app.utils.auth import create_access_token, authenticate_user
from motor.motor_asyncio import AsyncIOMotorClient
import os

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()
client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
db = client["transcription"]

@auth_router.post("/signup")
async def signup(user: UserIn):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user_dict = user.dict()
    user_dict["hashed_password"] = pwd_context.hash(user.password)
    user_dict.pop("password")
    user_dict["api_key"] = os.urandom(16).hex()
    result = await db.users.insert_one(user_dict)
    return {"message": "User created", "api_key": user_dict["api_key"]}

@auth_router.post("/login")
async def login(user: UserIn):
    db_user = await authenticate_user(user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user["email"]})
    return {"access_token": token, "token_type": "bearer"}
