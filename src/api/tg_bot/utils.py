import asyncio
import hashlib
import hmac
import json
import logging
from dataclasses import dataclass
from operator import itemgetter
from typing import Optional
from urllib.parse import parse_qsl

from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ChatMemberStatus
from aiogram.exceptions import (
    TelegramAPIError,
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramRetryAfter,
)

from config import BOT_TOKEN
from models.telegram import TelegramUser

logger = logging.getLogger(__name__)

@dataclass
class SendMessageResult:
    success: bool
    user_id: int
    deactivate: bool = False


def check_webapp_signature(token: str, init_data: str) -> bool:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token:
    :param init_data:
    :return:
    """
    try:
        parsed_data = dict(parse_qsl(init_data))
    except ValueError:
        # Init data is not a valid query string
        return False
    if "hash" not in parsed_data:
        # Hash is not present in init data
        return False

    hash_ = parsed_data.pop("hash")
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    user_id = eval(parsed_data["user"].replace("true", "True"))["id"]

    return {"status": calculated_hash == hash_, "user_id": user_id}


def check_webapp_signature_return_user(
    token: str, init_data: str
) -> TelegramUser:
    """
    Check incoming WebApp init data signature

    Source: https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    :param token:
    :param init_data:
    :return:
    """
    print(token, init_data)
    parsed_data = dict(parse_qsl(init_data))
    if "hash" not in parsed_data:
        # Hash is not present in init data
        print("hash not in parsed_data")
        return False

    hash_ = parsed_data.pop("hash")
    data_check_string = "\n".join(
        f"{k}={v}" for k, v in sorted(parsed_data.items(), key=itemgetter(0))
    )
    secret_key = hmac.new(
        key=b"WebAppData", msg=token.encode(), digestmod=hashlib.sha256
    )
    calculated_hash = hmac.new(
        key=secret_key.digest(),
        msg=data_check_string.encode(),
        digestmod=hashlib.sha256,
    ).hexdigest()

    user_data = json.loads(parsed_data["user"])
    
    return {
        "status": calculated_hash == hash_,
        "user": TelegramUser(
            start_param=parsed_data.get("start_param", None), **user_data
        ),
    }
 
 
async def send_hello_message_to_user(user_id: int):
    bot = Bot(token=BOT_TOKEN)
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Запустить 📲", url="https://t.me/traf_mediaBot/App")]
        ]
    )
    try:
        msg = await bot.send_photo(
            photo="AgACAgIAAxkBAAIY4GgYyjLzp3ytQgK8yCT9J6Iq-2LsAAJv9jEbWmzBSCZtKSv4l1WIAQADAgADeQADNgQ",
            caption="Добро пожаловать в <a href='https://t.me/traf_media'>Traffic Media</a> – агентство по продаже рекламы в Telegram и Instagram.\n\nЗаявите о себе на платежеспособную аудиторию с помощью рекламы в наших проектах.\n\nОзнакомиться с каждым по отдельности и взглянуть на цены можно в приложении ⇣",
            reply_markup=keyboard,
            chat_id=user_id,
            parse_mode="HTML"
        )
        await msg.pin()
    except Exception as e:
        logger.error(f"Error sending hello message to user {user_id}: {e}")
        return False
    return True

async def send_order_message_to_user(user: TelegramUser, text: str):
    bot = Bot(token=BOT_TOKEN)
    
    text = (
        f"<b>Информация о клиенте:</b>\n"
        f"ID: {user.id}\n"
        f"Имя: <a href='tg://user?id={user.id}'>{user.first_name}</a> (@{user.username})\n\n"
        f"<b>Информация о заказе:</b>\n"
        f"{text}" 
    )
    
    try:
        await bot.send_message(
            chat_id='-4704372354',
            text=text,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.error(f"Error sending order message to user {user.id}: {e}")
        return False
    return True
    
    