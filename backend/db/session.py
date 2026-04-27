from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy import text
from backend.config import get_settings
settings = get_settings
engine = create_async_engine(settings.database_url, echo=True, pool_size=10, max_overflow=20)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    db = async_session()
    try:
        yield db
        await db.commit()
    except:
        await db.rollback()
        raise
    finally:
        db.close()