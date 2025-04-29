import boto3
from botocore.exceptions import ClientError
import os
import logging

logger = logging.getLogger(__name__)

def get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def upload_file_to_s3(file_content, file_name):
    bucket_name = "practica-5-745369"
    s3_client = get_s3_client()

    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=file_content
        )

        s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
        logger.info(f"File uploaded successfully to S3: {s3_url}")
        return s3_url

    except ClientError as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise Exception(f"S3 upload error: {str(e)}")
