import uuid

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(String, default="", nullable=False)
    profile_image_url: Mapped[str] = mapped_column(String, default="", nullable=False)
    followers: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    following: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)

    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
