from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from database.repo.giveaways import GiveawaysRepo
from database.repo.channels import ChannelsRepo
from database.repo.user_login import UserLoginRepo
from database.repo.users import UsersRepo
from database.repo.mailing import MailingRepo  


@dataclass
class RequestsRepo:
    session: AsyncSession

    @property
    def users(self):
        return UsersRepo(self.session)

    @property
    def user_login(self):
        return UserLoginRepo(self.session)
    
    @property
    def giveaways(self):
        return GiveawaysRepo(self.session)
    
    @property
    def channels(self):
        return ChannelsRepo(self.session)
    
    @property
    def mailings(self):
        return MailingRepo(self.session)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self):
        await self.session.flush()

