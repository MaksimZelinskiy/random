from database.models.admins import Admin
from database.repo.base import BaseRepo
from sqlalchemy import select

class AdminsRepo(BaseRepo):
    async def get_admin_by_id(self, admin_id: int) -> Admin:
        query = select(Admin).where(Admin.id == admin_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_admin_by_username(self, username: str) -> Admin:
        query = select(Admin).where(Admin.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
