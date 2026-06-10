from fastapi import APIRouter

from app.schemas.ai import (
    SuggestRepliesRequest,
    SuggestRepliesResponse,
    SummarizeRequest,
    SummarizeResponse,
)
from app.services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/summarize")
async def summarize(payload: SummarizeRequest) -> SummarizeResponse:
    summary = await ai_service.summarize(payload.text)
    return SummarizeResponse(summary=summary)


@router.post("/suggest-replies")
async def suggest_replies(
    payload: SuggestRepliesRequest,
) -> SuggestRepliesResponse:
    replies = await ai_service.suggest_replies(payload.message)
    return SuggestRepliesResponse(replies=replies)
