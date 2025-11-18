from sqlalchemy.ext.asyncio import AsyncSession
from .connection import async_session


async def get_db() -> AsyncSession:

    async with async_session() as session:
        try:
            yield session
        except Exception as exc:
            await session.rollback()
            raise exc
        finally:
            await session.close()