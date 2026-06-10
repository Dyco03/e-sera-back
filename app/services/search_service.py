from app.repositories.user_repository import UserRepository
from app.services.user_mapper import user_to_profile


class SearchService:
    def __init__(self, users: UserRepository):
        self.users = users

    def search_users(self, query: str) -> dict:
        if not query:
            return {"users": [], "data": []}

        users = [user_to_profile(user) for user in self.users.search_by_name(query)]
        return {"users": users, "data": users}
