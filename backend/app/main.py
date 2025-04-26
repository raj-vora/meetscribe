from fastapi import FastAPI
from app.routes import meetings, transcribe
from app.auth import auth_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth_router)
app.include_router(meetings.router)
app.include_router(transcribe.router)