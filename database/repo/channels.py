import logging
from typing import Any
from datetime import date, time

from sqlalchemy import insert, select, update, func, delete

from database.models.admins import AdminChannelBind

from .base import BaseRepo

logger = logging.getLogger(__name__)



class ChannelsRepo(BaseRepo):

    async def get_channels_by_admin_id(self, admin_id: int) -> list[AdminChannelBind]:
        query = select(AdminChannelBind).where(AdminChannelBind.admin_id == admin_id).order_by(AdminChannelBind.created_at.desc())
        res = await self.session.execute(query)
        return res.scalars().all()

    async def bind_channel_to_admin(
        self,
        admin_id: int,
        channel_id: str,
        channel_title: str,
        channel_username: str,
        channel_link: str,
    ):
        logger.info(f"Binding channel {channel_id} to admin {admin_id}")

        query = insert(AdminChannelBind).values(
            admin_id=admin_id,
            channel_id=channel_id,
            channel_title=channel_title,
            channels_username=channel_username,
            channels_link=channel_link,
            channel_status="active",
        )

        await self.session.execute(query)
        
    async def unbind_channel_from_admin(
        self,
        admin_id: int,
        channel_id: int,
    ):
        query = delete(AdminChannelBind).where(AdminChannelBind.admin_id == admin_id, AdminChannelBind.channel_id == channel_id)
        await self.session.execute(query) 
        
    async def get_channel_by_id(self, channel_id: int) -> AdminChannelBind | None:
        query = select(AdminChannelBind).where(AdminChannelBind.channel_id == channel_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()

    
    
    async def update_status_channel(self, admin_id: int, channel_id: str, status: str):
        query = update(AdminChannelBind).where(AdminChannelBind.admin_id == admin_id, AdminChannelBind.channel_id == channel_id).values(channel_status=status)
        await self.session.execute(query)


    async def delete_channel(self, channel_id: str):
        query = delete(AdminChannelBind).where(AdminChannelBind.channel_id == channel_id)
        await self.session.execute(query)
        
        
    async def get_active_channels_by_admin_id(self, admin_id: int) -> list[AdminChannelBind]:
        query = select(AdminChannelBind).where(AdminChannelBind.admin_id == admin_id, AdminChannelBind.channel_status == "active")
        res = await self.session.execute(query)
        return res.scalars().all()
    
    async def get_channels_by_ids(self, channel_ids: list[int]) -> list[AdminChannelBind]:
        query = select(AdminChannelBind).where(AdminChannelBind.channel_id.in_(channel_ids))
        res = await self.session.execute(query)
        return res.scalars().all()      