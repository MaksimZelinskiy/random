from fastapi import HTTPException, Request, Depends

from tg_bot.utils import (
    check_webapp_signature,
    check_webapp_signature_return_user,
)
from config import BOT_TOKEN
from database import get_session_pool, RequestsRepo
from models.telegram import TelegramUser



from sqlalchemy.ext.asyncio import AsyncSession
from database.setup import get_session_pool

async def get_session() -> AsyncSession:
    async_session = get_session_pool()
    async with async_session() as session:
        yield session

async def get_repo(session: AsyncSession = Depends(get_session)) -> RequestsRepo:
    return RequestsRepo(session)

def get_user_id_from_webdata(request: Request) -> int:
    if request.query_params.get("test"):
        return 353357144
    elif request.query_params.get("test_user_id"):
        return int(request.query_params.get("test_user_id", 353357144))
    else:
        result = check_webapp_signature(
            BOT_TOKEN, request.query_params.get("initData")
        )
        if result:
            return result["user_id"]
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")


def get_user_from_webdata(request: Request) -> TelegramUser:
    if request.query_params.get("test"):
        return TelegramUser(
            id=353357144,
            first_name="Test",
            last_name="User",
            username="test_user",
        )
    elif request.query_params.get("test_user_id"):
        return TelegramUser(
            id=int(request.query_params.get("test_user_id", 353357144)),
            first_name="Test",
            last_name="User",
            username="test_user",
        )
    else:
        print(f"tyt {request.query_params.get('initData')}")
        result = check_webapp_signature_return_user(
            BOT_TOKEN, request.query_params.get("initData")
        )
        print(result)
        if result["status"]:
            return result["user"]
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
