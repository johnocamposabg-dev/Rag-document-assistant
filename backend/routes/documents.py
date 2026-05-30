from typing import Annotated
from fastapi import File, UploadFile, APIRouter

router = APIRouter()

@router.post("/upload/")
async def create_upload_file(file: UploadFile):
        pass
