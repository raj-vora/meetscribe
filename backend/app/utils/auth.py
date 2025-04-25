from jose import jwt
from passlib.context import CryptContext
from motor.motor_asyncio import AsyncIOMotorClient
import os

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
db = client["transcription"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def authenticate_user(email, password):
    user = await db.users.find_one({"email": email})
    if user and pwd_context.verify(password, user["hashed_password"]):
        return user
    return None

def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)