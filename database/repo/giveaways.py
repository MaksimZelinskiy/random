import logging
from typing import Any
from datetime import date, time, datetime, timedelta

from sqlalchemy import insert, select, update, func, delete, text

from database.models.giveaways import Giveaway, GiveawayWinner

from .base import BaseRepo

logger = logging.getLogger(__name__)



class GiveawaysRepo(BaseRepo):

    async def get_giveaways_by_admin_id(self, admin_id: int) -> list[Giveaway]:
        query = select(Giveaway).where(Giveaway.admin_id == admin_id).order_by(Giveaway.created_at.desc())
        res = await self.session.execute(query)
        return res.scalars().all()

    async def create_giveaway(
        self,
        admin_id: int,
        publish_channels: list[str],
        required_channels: list[str],
        view_details: dict,
        count_winners: int,
        use_boost: bool,
        use_capha: bool,
        use_block_twinks: bool,
        start_at: datetime,
        ends_at: datetime,
    ):

        query = insert(Giveaway).values(
            admin_id=admin_id,
            publish_channels=publish_channels,
            required_channels=required_channels,
            view_details=view_details,
            count_winners=count_winners,
            use_boost=use_boost,
            use_capha=use_capha,
            use_block_twinks=use_block_twinks,
            start_at=start_at,
            ends_at=ends_at,
        )

        await self.session.execute(query)
        
    async def get_giveaway_by_id(self, giveaway_id: str) -> Giveaway | None:
        query = select(Giveaway).where(Giveaway.id == giveaway_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()
    
    async def get_giveaway_by_id_and_admin_id(self, giveaway_id: str, admin_id: int) -> Giveaway | None:
        query = select(Giveaway).where(Giveaway.id == giveaway_id, Giveaway.admin_id == admin_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()
    
    async def get_giveaways_by_start_is_not_published(self) -> list[Giveaway]:
        query = select(Giveaway).where(Giveaway.start_at > func.now(), Giveaway.is_published == False)
        res = await self.session.execute(query)
        return res.scalars().all()
    
    async def get_giveaways_for_winners_selection(self) -> list[Giveaway]:
        query = select(Giveaway).where(Giveaway.ends_at < func.now() + timedelta(minutes=10), Giveaway.status == "active")
        res = await self.session.execute(query)
        return res.scalars().all()
    
    
    async def get_active_giveaways_by_admin_id(self, admin_id: int) -> list[Giveaway]:
        query = select(Giveaway).where(Giveaway.admin_id == admin_id, Giveaway.status == "active")
        res = await self.session.execute(query)
        return res.scalars().all()    
    
    async def get_giveaway_winners_by_giveaway_id(self, giveaway_id: str) -> list[GiveawayWinner]:
        query = select(GiveawayWinner).where(GiveawayWinner.giveaway_id == giveaway_id)
        res = await self.session.execute(query)
        return res.scalars().all()
    
    async def add_giveaway_winner(self, giveaway_id: str, user_id: int, place: int, type: str):
        query = insert(GiveawayWinner).values(
            giveaway_id=giveaway_id,
            user_id=user_id,
            place=place,
            type=type
        )
        await self.session.execute(query)