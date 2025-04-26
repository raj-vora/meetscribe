from fastapi import APIRouter, Depends, HTTPException
from app.utils.auth import authenticate_user, get_current_user
from motor.motor_asyncio import AsyncIOMotorClient
import os
from bson import ObjectId

router = APIRouter()
client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
db = client["meetscribe"]

@router.get("/meetings")
async def get_meetings(current_user = Depends(get_current_user)):
    meetings = await db.meetings.find().to_list(100)
    return meetings

@router.get("/meetings/{id}/transcription")
async def get_transcription(id: str, current_user = Depends(get_current_user)):
    result = await db.transcriptions.find_one({"meeting_id": id})
    if not result:
        raise HTTPException(status_code=404, detail="Transcription not found")
    return result