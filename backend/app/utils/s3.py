import boto3
import os
from uuid import uuid4

s3 = boto3.client("s3", aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                  aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

async def upload_audio_to_s3(file):
    s3.upload_fileobj(file.file, os.environ["S3_BUCKET"], file.filename)
    url = f"https://{os.environ['S3_BUCKET']}.s3.amazonaws.com/{file.filename}"

async def get_file_from_s3(key: str):
    """
    Fetch a file from S3 using its key.
    
    Args:
        key (str): The S3 key of the file to fetch
        
    Returns:
        bytes: The file content as bytes
    """
    response = s3.get_object(Bucket=os.environ["S3_BUCKET"], Key=key)
    return response['Body'].read()

   
