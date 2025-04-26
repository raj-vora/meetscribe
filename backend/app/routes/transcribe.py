from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends
from app.utils.s3 import upload_audio_to_s3
from app.transcription_task import run_transcription
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...), 
    background_tasks: BackgroundTasks = BackgroundTasks(),
    current_user = Depends(get_current_user)
):
    await upload_audio_to_s3(file)
    background_tasks.add_task(run_transcription, file.filename, current_user['email'])
    return {"message": "File uploaded and transcription queued."}