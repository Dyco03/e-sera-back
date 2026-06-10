from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.messages import (
    ConversationsResponse,
    MessageCreateRequest,
    MessageOut,
    MessagesResponse,
)
from app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


def _service(db: Session) -> MessageService:
    return MessageService(MessageRepository(db), UserRepository(db))


@router.get("/conversations/{user_id}")
def list_conversations(
    user_id: str,
    db: Session = Depends(get_db),
) -> ConversationsResponse:
    return ConversationsResponse(**_service(db).list_conversations(user_id))


@router.get("/thread")
def list_thread(
    currentUserId: str = Query(...),
    otherUserId: str = Query(...),
    db: Session = Depends(get_db),
) -> MessagesResponse:
    return MessagesResponse(**_service(db).list_thread(currentUserId, otherUserId))


@router.post("")
def send_message(
    payload: MessageCreateRequest,
    db: Session = Depends(get_db),
) -> MessageOut:
    result = _service(db).send_message(payload)
    return MessageOut(**result["message"])
