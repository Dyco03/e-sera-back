from fastapi import APIRouter, File, UploadFile

from app.services.storage_service import StorageService

router = APIRouter(prefix="/storage", tags=["storage"])


@router.post("/profile-images")
async def upload_profile_image(file: UploadFile = File(...)) -> dict:
    return await StorageService().save_upload(file, "profile-images")


@router.post("/post-images")
async def upload_post_image(file: UploadFile = File(...)) -> dict:
    return await StorageService().save_upload(file, "post-images")
