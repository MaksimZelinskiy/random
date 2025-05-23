import logging
from datetime import date, timedelta

from database.models.users import User
from database import RequestsRepo
from models.telegram import TelegramUser

logger = logging.getLogger(__name__)


class UsersClient:
    def __init__(self, repo: RequestsRepo, user: TelegramUser):
        self.repo = repo
        self.user = user

    async def track_user_login(
        self, user_id: int, user_ip: str, startapp_code: str
    ):
        await self.repo.user_login.track_user_login(
            user_id, {"startapp_code": startapp_code}
        )
        await self.repo.commit()

    async def update_user_ip(self, user_id: int, user_ip: str):
        await self.repo.users.update_user_ip(user_id, user_ip)
        await self.repo.commit()

    async def register_user(self, user: TelegramUser, startup_code: str):
        await self.repo.users.create_user(
            user.id,
            user.username,
            user.first_name,
            user.language_code,
            startup_code,
        )

    async def get_user_if_exists(self, user_id: int) -> User | None:
        return await self.repo.users.get_user_if_exists(user_id)

    async def get_user(self, user_id: int) -> User | None:
        return await self.repo.users.get_user(user_id)
