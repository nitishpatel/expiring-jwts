from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from expiring_jwts.core.config import DATABASE_URL

# Use async engine instead of sync engine
engine = create_async_engine(DATABASE_URL, pool_size=20, max_overflow=1, pool_recycle=3600)

# Use AsyncSession for async queries
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
