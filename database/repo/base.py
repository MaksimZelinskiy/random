from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepo:
    """
    A class representing a base repository for handling database operations.

    Attributes:
        session (AsyncSession): The database session used by the repository.

    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def commit(self):
        await self.session.commit()
