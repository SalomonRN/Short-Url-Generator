from app.core.db.repositories.interface import URLRepository
from sqlalchemy.ext.asyncio import AsyncSession

class PostgresUrlRepository(URLRepository):
    def __init__(self, db_session: AsyncSession):
        super().__init__()
        self.db_session = db_session
        raise NotImplementedError()

    async def get_url(self, tiny_url: str):
        raise NotImplementedError()
