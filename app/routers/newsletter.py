from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import uuid
from app.services.s3_service import upload_file_to_s3
from app.services.sqs_service import send_message_to_sqs

router = APIRouter(
    prefix="/newsletters",
    tags=["newsletters"],
)

@router.post("/")
async def create_newsletter(
    file: UploadFile = File(...),
    message: str = Form(...),
    email: str = Form(...)
):
    try:
        file_extension = file.filename.split(".")[-1] if "." in file.filename else ""
        unique_filename = f"{uuid.uuid4()}.{file_extension}"

        file_content = await file.read()
        s3_url = upload_file_to_s3(file_content, unique_filename)

        message_data = {
            "email": email,
            "message": message,
            "image_url": s3_url
        }

        send_message_to_sqs(message_data)

        return {
            "status": "success",
            "message": "Newsletter processed successfully",
            "details": {
                "email": email,
                "image_url": s3_url
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing newsletter: {str(e)}")
