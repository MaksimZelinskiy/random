import logging
from typing import Any
from datetime import date, time, datetime, timedelta

from sqlalchemy import insert, select, update, func, delete, text

from database.models.users import UserMailings

from .base import BaseRepo

logger = logging.getLogger(__name__)



class MailingRepo(BaseRepo):

    async def get_mailings_by_datetime(self, now: datetime, limit: int = 100, task_types: list[str] = ["mailing"]) -> list[UserMailings]:
        
        query = select(UserMailings).where(UserMailings.scheduled_at < now).where(UserMailings.task_type.in_(task_types)).where(UserMailings.status == "pending").order_by(UserMailings.created_at).limit(limit)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def create_mailing(
        self,
        created_by_admin_id: int,
        task_type: str,
        target_id: str,
        message_type: str,
        media_file_id: str | None,
        text: str,
        reply_markup: dict | None,
        scheduled_at: datetime,
    ):

        query = insert(UserMailings).values(
            created_by_admin_id=created_by_admin_id,
            task_type=task_type,
            target_id=target_id,
            message_type=message_type,
            media_file_id=media_file_id,
            text=text,
            reply_markup=reply_markup,
            scheduled_at=scheduled_at,
        )

        await self.session.execute(query)
      
    async def update_mailing_status(self, mailing: UserMailings, status: str, error_message: str = None, msg_id: int | None = None):   
        query = (
            update(UserMailings)
            .where(UserMailings.id == mailing.id)
            .values(status=status, error_message=error_message, msg_id=msg_id)
        )
        await self.session.execute(query)   
    
        
        
        
