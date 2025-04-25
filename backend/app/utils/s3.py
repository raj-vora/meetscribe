import boto3
import os
from uuid import uuid4

s3 = boto3.client("s3", aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

async def upload_audio_to_s3(file):
    key = f"audio/{uuid4()}.wav"
    s3.upload_fileobj(file.file, os.environ["S3_BUCKET"], key)
    url = f"https://{os.environ['S3_BUCKET']}.s3.amazonaws.com/{key}"
    return url
