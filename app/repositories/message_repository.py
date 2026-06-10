from sqlalchemy import and_, or_, select
from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_for_user(self, user_id: str) -> list[Message]:
        statement = (
            select(Message)
            .where(or_(Message.sender_id == user_id, Message.receiver_id == user_id))
            .order_by(Message.timestamp.desc())
        )
        return list(self.db.scalars(statement))

    def list_thread(self, current_user_id: str, other_user_id: str) -> list[Message]:
        statement = (
            select(Message)
            .where(
                or_(
                    and_(
                        Message.sender_id == current_user_id,
                        Message.receiver_id == other_user_id,
                    ),
                    and_(
                        Message.sender_id == other_user_id,
                        Message.receiver_id == current_user_id,
                    ),
                )
            )
            .order_by(Message.timestamp.asc())
        )
        return list(self.db.scalars(statement))

    def create(self, message: Message) -> Message:
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
