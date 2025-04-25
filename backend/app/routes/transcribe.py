from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from app.utils.s3 import upload_audio_to_s3
from app.transcription_task import run_transcription

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks()):
    s3_url = await upload_audio_to_s3(file)
    background_tasks.add_task(run_transcription, s3_url)
    return {"message": "File uploaded and transcription queued."}