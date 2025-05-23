from sqlalchemy import insert, select, func, cast, distinct
from sqlalchemy import Date

from datetime import date, timedelta

from database.models.users import UserLogin

from .base import BaseRepo


class UserLoginRepo(BaseRepo):
    async def track_user_login(
        self, user_id: int, data: dict
    ):
        query = insert(UserLogin).values(
            user_id=user_id, data=data
        )

        await self.session.execute(query)

    async def get_recent_stats_logins(self, days: int) -> list[tuple[date, int]]:
        query = (
            select(
                func.date(UserLogin.created_at).label('date'),
                func.count(distinct(UserLogin.user_id)).label('count')
            )
            .group_by(func.date(UserLogin.created_at))
            .order_by(func.date(UserLogin.created_at).desc())
            .limit(days)
        )
        res = await self.session.execute(query)
        return res.fetchall()

    async def track_user_mailing(
        self, user_id: int, data: dict
    ):
        query = insert(UserLogin).values(
            user_id=user_id, data=data
        )

        await self.session.execute(query)
