from fastapi import HTTPException, status

from app.models.message import Message
from app.repositories.message_repository import MessageRepository
from app.repositories.user_repository import UserRepository
from app.schemas.messages import MessageCreateRequest


class MessageService:
    def __init__(self, messages: MessageRepository, users: UserRepository):
        self.messages = messages
        self.users = users

    def list_conversations(self, user_id: str) -> dict:
        self._get_user_or_404(user_id)
        latest_by_user: dict[str, Message] = {}

        for message in self.messages.list_for_user(user_id):
            other_user_id = (
                message.receiver_id if message.sender_id == user_id else message.sender_id
            )
            if other_user_id not in latest_by_user:
                latest_by_user[other_user_id] = message

        conversations = [
            self._conversation_to_dict(user_id, other_user_id, message)
            for other_user_id, message in latest_by_user.items()
        ]
        return {"conversations": conversations, "data": conversations}

    def list_thread(self, current_user_id: str, other_user_id: str) -> dict:
        self._get_user_or_404(current_user_id)
        self._get_user_or_404(other_user_id)

        messages = [
            self._message_to_dict(message)
            for message in self.messages.list_thread(current_user_id, other_user_id)
        ]
        return {"messages": messages, "data": messages}

    def send_message(self, payload: MessageCreateRequest) -> dict:
        sender = self._get_user_or_404(payload.senderId)
        self._get_user_or_404(payload.receiverId)
        text = payload.text.strip()

        if payload.senderId == payload.receiverId:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Cannot send a message to yourself",
            )
        if not text:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Message cannot be empty",
            )

        message = Message(
            sender_id=sender.id,
            receiver_id=payload.receiverId,
            text=text,
        )
        saved = self.messages.create(message)
        data = self._message_to_dict(saved)
        return {"message": data, "data": data}

    def _get_user_or_404(self, user_id: str):
        user = self.users.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user

    def _conversation_to_dict(
        self,
        current_user_id: str,
        other_user_id: str,
        last_message: Message,
    ) -> dict:
        other_user = self._get_user_or_404(other_user_id)
        return {
            "otherUserId": other_user.id,
            "otherUserName": other_user.name,
            "otherUserEmail": other_user.email,
            "otherUserProfileImageUrl": other_user.profile_image_url,
            "lastMessage": self._message_to_dict(last_message),
        }

    def _message_to_dict(self, message: Message) -> dict:
        return {
            "id": message.id,
            "senderId": message.sender_id,
            "receiverId": message.receiver_id,
            "text": message.text,
            "timestamp": message.timestamp,
        }
