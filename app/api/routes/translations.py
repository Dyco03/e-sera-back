from fastapi import APIRouter

from app.schemas.translations import PostTranslationRequest, PostTranslationResponse
from app.services.translation_service import translation_service

router = APIRouter(prefix="/translations", tags=["translations"])


@router.post("/post")
async def translate_post(payload: PostTranslationRequest) -> PostTranslationResponse:
    result = await translation_service.translate_post(
        payload.text,
        payload.targetLanguage,
    )
    return PostTranslationResponse(**result)
