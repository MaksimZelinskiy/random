# setup.py

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncEngine

DB_HOST, DB_NAME, DB_PASSWORD, DB_USER, DB_PORT = (
    "database", "random", "com265", "com_user", 5432
)

POSTGRES_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# создаётся один раз
engine: AsyncEngine = create_async_engine(
    POSTGRES_URL,
    query_cache_size=1200,
    pool_size=50,
    max_overflow=200,
    future=True,
    echo=False,
)

session_pool = async_sessionmaker(bind=engine, expire_on_commit=False)

def get_session_pool():
    return session_pool

async def close_engine():
    await engine.dispose()
