import asyncio
from datetime import datetime
from typing import Optional
from limiter import RATE_LIMITER

from database.models.users import UserMailings
from database.repo.requests import RequestsRepo

from config import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest, TelegramAPIError 
from utils_system.tg import TG_BOT

logger = logging.getLogger(__name__)

async def send_message_by_type_to_user(
    mailing: UserMailings,
) -> tuple[bool, Message, UserMailings, str]:
    """
    Отправляет сообщение пользователю с указанным типом (текст или фото)

    Args:
        repo: Репозиторий для работы с БД
        user_id: ID пользователя
        mailing: Объект UserMailings

    Returns:
        SendMessageResult с результатом отправки
    """
    user_id = mailing.target_id
    try:
        buttons = []
        
        for button in mailing.reply_markup:
            buttons.append([InlineKeyboardButton(text=button['text'], callback_data=button['data'] if 'data' in button else None, url=button['url'] if 'url' in button else None)])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None
        
        match mailing.message_type:
            case "text":
                msg = await TG_BOT.send_message(
                    chat_id=user_id,
                    text=mailing.text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
            case "photo":
                msg = await TG_BOT.send_photo(
                    chat_id=user_id,
                    photo=mailing.media_file_id,
                    caption=mailing.text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
            case "video":
                msg = await TG_BOT.send_video(
                    chat_id=user_id,
                    video=mailing.media_file_id,
                    caption=mailing.text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )   
            case "animation":
                msg = await TG_BOT.send_animation(
                    chat_id=user_id,
                    animation=mailing.media_file_id,
                    caption=mailing.text,
                    reply_markup=keyboard,
                )   
            case _:
                logger.error(f"Неподдерживаемый тип сообщения: {mailing.message_type}")
                return False, None, mailing, "Неподдерживаемый тип сообщения"

        return True, msg, mailing, "Успешно отправлено"

    except TelegramRetryAfter as e:
        logger.warning(
            f"Превышен лимит запросов для пользователя {user_id}, повтор через {e.retry_after} сек"
        )
        await asyncio.sleep(e.retry_after)
        return await send_message_by_type_to_user(
            user_id=user_id,
            mailing=mailing
        )

    except (TelegramBadRequest, TelegramAPIError) as e:
        logger.error(
            f"Ошибка Telegram API для пользователя {user_id}: {str(e)}"
        )
        return False, None, mailing, f"Ошибка Telegram API ({str(e)})"

    # except Exception as e:
    #     logger.error(
    #         f"Непредвиденная ошибка при отправке сообщения пользователю {user_id}: {str(e)}"
    #     )
    #     return False, None, mailing, f"Непредвиденная ошибка ({str(e)})"

