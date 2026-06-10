from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreateRequest(BaseModel):
    senderId: str
    receiverId: str
    text: str = Field(min_length=1)


class MessageOut(BaseModel):
    id: str
    senderId: str
    receiverId: str
    text: str
    timestamp: datetime


class ConversationOut(BaseModel):
    otherUserId: str
    otherUserName: str
    otherUserEmail: str
    otherUserProfileImageUrl: str = ""
    lastMessage: MessageOut


class MessagesResponse(BaseModel):
    messages: list[MessageOut]
    data: list[MessageOut]


class ConversationsResponse(BaseModel):
    conversations: list[ConversationOut]
    data: list[ConversationOut]
