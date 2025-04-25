import whisper
from pyannote.audio import Pipeline
import os
from datetime import timedelta
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
db = client["transcription"]

def get_speaker_label(diarization, time_sec):
    for turn in diarization.itertracks(yield_label=True):
        segment, _, speaker = turn
        if segment.start <= time_sec <= segment.end:
            return speaker
    return "Unknown"

async def run_transcription(audio_path):
    whisper_model = whisper.load_model("small")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=os.environ.get("HF_TOKEN"))
    diarization = pipeline(audio_path)
    result = whisper_model.transcribe(audio_path)

    blocks = []
    for segment in result['segments']:
        start = segment['start']
        end = segment['end']
        speaker = get_speaker_label(diarization, start)
        blocks.append({
            "speaker": speaker,
            "start": start,
            "end": end,
            "text": segment['text']
        })

    await db.transcriptions.insert_one({
        "meeting_id": audio_path,  # Use actual meeting ID in production
        "transcription": blocks
    })