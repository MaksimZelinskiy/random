import logging
from typing import Any
from datetime import date, time

from sqlalchemy import insert, select, update, func

from database.models.users import User

from .base import BaseRepo

logger = logging.getLogger(__name__)



class UsersRepo(BaseRepo):
    async def update_user_by_id(self, user_id: int, col: str, value: Any):
        query = (
            update(User).where(User.user_id == user_id).values({col: value})
        )

        await self.session.execute(query)

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()

    async def create_user(
        self,
        user_id: int,
        username: str,
        name: str,
        language: str,
        referrer_id: str,
    ):
        logger.info(f"Creating user {user_id} with refferer id {referrer_id}")

        query = insert(User).values(
            user_id=user_id,
            username=username,
            name=name,
            lang=language,
            referrer_id=referrer_id
        )

        await self.session.execute(query)

    async def get_users_by_status(self, status: str) -> list[User]:
        query = select(User).where(User.status == status)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_user_if_exists(self, user_id: int) -> User | None:  
        query = select(User).where(User.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()

    async def get_detailed_stats_utm_codes(self) -> list[tuple[int, str]]:
        query = select(func.count(User.user_id), User.referrer_id).group_by(User.referrer_id)
        res = await self.session.execute(query)
        return res.fetchall()


    async def get_language_stats(self) -> list[tuple[str, int]]:
        query = select(User.lang, func.count(User.user_id)).group_by(User.lang)
        res = await self.session.execute(query)
        return res.fetchall()


    async def get_recent_stats(self, days: int) -> list[tuple[date, int]]:
        """Get registration statistics for recent days."""
        query = (
            select(
                func.date(User.date_reg).label('date'),
                func.count(User.user_id).label('count')
            )
            .group_by(func.date(User.date_reg))
            .order_by(func.date(User.date_reg).desc())
            .limit(days)
        )
        res = await self.session.execute(query)
        return res.fetchall()


    async def get_users_for_mailing(self, time_mailing: time) -> list[User]:
        query = select(User).where(User.status == "active", User.time_mailing <= time_mailing.hour)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_users_for_mailing_calendar(self) -> list[User]:
        query = select(User).where(User.status == "active", User.date_birthday is not None)
        res = await self.session.execute(query)
        return res.scalars().all()  

