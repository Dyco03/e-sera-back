from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.search_service import SearchService

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/users")
def search_users(q: str = Query(default=""), db: Session = Depends(get_db)) -> dict:
    return SearchService(UserRepository(db)).search_users(q)
