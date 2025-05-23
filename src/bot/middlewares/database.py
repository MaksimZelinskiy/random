import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, ChatMemberUpdated

from database.repo.requests import RequestsRepo

log = logging.getLogger(__name__)


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool) -> None:
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            repo = RequestsRepo(session)

            data["session"] = session
            data["repo"] = repo
            
            if isinstance(event, Message):
                text = event.text if event.text else "no_text"
                await repo.user_login.track_user_login(
                    event.from_user.id, 
                    {
                        "type": "message",
                        "result": text
                    }
                )
            

            elif isinstance(event, CallbackQuery):
                callback_data = event.data if event.data else "no_data" 
                await repo.user_login.track_user_login(
                    event.from_user.id, 
                    {
                        "type": "callback",
                        "result": callback_data
                    }
                )
            await repo.commit()
            

            result = await handler(event, data)
        return result
