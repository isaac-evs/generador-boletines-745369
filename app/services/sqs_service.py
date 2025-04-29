import boto3
import json
import os
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def get_sqs_client():
    return boto3.client(
        'sqs',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION', 'us-east-1')
    )

def send_message_to_sqs(message_data):
    queue_name = "cola-boletines"
    sqs_client = get_sqs_client()

    try:
        response = sqs_client.get_queue_url(QueueName=queue_name)
        queue_url = response['QueueUrl']

        message_body = json.dumps(message_data)
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body
        )

        logger.info(f"Message sent to SQS queue: {queue_name}")
        return response

    except ClientError as e:
        logger.error(f"Error sending message to SQS: {e}")
        raise Exception(f"SQS send error: {str(e)}")
