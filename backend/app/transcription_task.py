from datetime import datetime
import whisper
from pyannote.audio import Pipeline
import os
from motor.motor_asyncio import AsyncIOMotorClient
from app.utils.s3 import get_file_from_s3

client = AsyncIOMotorClient(os.environ.get("MONGO_URI"))
db = client["meetscribe"]

def get_speaker_label(diarization, time_sec):
    for turn in diarization.itertracks(yield_label=True):
        segment, _, speaker = turn
        if segment.start <= time_sec <= segment.end:
            return speaker
    return "Unknown"

async def run_diarization(file, local_path):
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=os.environ.get("HF_TOKEN"))
    diarization = pipeline(local_path)

    await db.transcriptions.update_one(
        {"meeting_id": file},
        {"$set": {"status": "diarized", "updated_at": datetime.utcnow()}},
        upsert=True
    )

    # Save diarization result to a file
    diar_file = local_path.replace(".wav", "_diar.rttm")
    with open(diar_file, "w") as f:
        diarization.write_rttm(f)
    print("done diarizing")
    return diarization

async def run_transcription(file, user):
    tmp_dir = os.path.join(os.getcwd(), "tmp_audio")
    os.makedirs(tmp_dir, exist_ok=True)
    local_path = os.path.join(tmp_dir, os.path.basename(file))
    file_record = await db.transcriptions.find_one({"meeting_id": file})

    # Step 1: If not uploaded, download and mark as uploaded
    if not file_record or file_record.get("status") not in ["uploaded", "diarized", "transcribed"]:
        file_content = await get_file_from_s3(file)
        with open(local_path, 'wb') as f:
            f.write(file_content)

        await db.transcriptions.update_one(
            {"meeting_id": file},
            {"$set": {"user": user,"status": "uploaded", "created_at": datetime.utcnow()}},
            upsert=True
        )

    # Step 2: Run diarization if not done yet
    if not file_record or file_record.get("status") in ["uploaded"]:
        diarization = await run_diarization(file, local_path)
    else:
        # Optionally re-load diarization if already diarized
        print("diarized, will now transcribe")
        diarization = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1", use_auth_token=os.environ.get("HF_TOKEN")
        )(local_path)

    # Step 3: Run transcription if not done
    if not file_record or file_record.get("status") != "transcribed":
        whisper_model = whisper.load_model("small", in_memory=True)
        result = whisper_model.transcribe(local_path)

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

        await db.transcriptions.update_one(
            {"meeting_id": file},
            {"$set": {
                "status": "transcribed",
                "transcription": blocks,
                "updated_at": datetime.utcnow()
            }},
        )
    print("Transcribed!")

    # Clean up only if not skipping any step
    if os.path.exists(local_path):
        os.remove(local_path)
