from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


class StorageService:
    async def save_upload(self, file: UploadFile, folder: str) -> dict:
        upload_dir = settings.upload_dir / folder
        upload_dir.mkdir(parents=True, exist_ok=True)

        suffix = Path(file.filename or "").suffix
        filename = f"{uuid4()}{suffix}"
        destination = upload_dir / filename

        contents = await file.read()
        destination.write_bytes(contents)

        url = f"{settings.public_base_url}/uploads/{folder}/{filename}"
        return {"url": url, "publicUrl": url, "data": url}
