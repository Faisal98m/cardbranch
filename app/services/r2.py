import boto3
import os
from botocore.config import Config

def get_r2_client():
    return boto3.client(
        's3',
        endpoint_url=f"https://{os.environ['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
        aws_access_key_id=os.environ['R2_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['R2_SECRET_ACCESS_KEY'],
        config=Config(signature_version='s3v4'),
        region_name='auto',
    )

def upload_file(local_path, r2_key):
    client = get_r2_client()
    bucket = os.environ['R2_BUCKET_NAME']
    content_type = 'application/pdf' if local_path.endswith('.pdf') else 'image/png'
    client.upload_file(local_path, bucket, r2_key, ExtraArgs={'ContentType': content_type})
    public_url = os.environ['R2_PUBLIC_URL'].rstrip('/')
    return f"{public_url}/{r2_key}"
