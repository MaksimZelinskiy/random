import asyncio
from datetime import datetime
import logging
import os 

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardMarkup, KeyboardButton, FSInputFile   
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext

from filters import IsPrivate
from loader import bot
from tg_utils import texts, keyboards
from utils import message as message_utils
from data import config
from database.repo.requests import RequestsRepo
from database.models.offers import OFFER_STATUS_SYMBOLS, OFFER_STATUS_TEXTS

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, repo: RequestsRepo):
    user = await repo.users.get_user_if_exists(callback.from_user.id)
    user_balance = await repo.balance.get_user_balance_by_user_id_if_exists(callback.from_user.id)
    
    if not user:
        await callback.answer("Вы не авторизованы")
        return
    
    if not user_balance:
        await repo.balance.create_user_balance(
            user_id=callback.from_user.id,
            amount=0
        )
        user_balance = await repo.balance.get_user_balance_by_user_id_if_exists(
            callback.from_user.id
        )
    
    keyboard = await keyboards.ProfileKeyboard().main()

    await message_utils.send_message(
        callback.message,
        texts.PROFILE["main"].format(
            user_id=user.user_id,
            user_balance=user_balance.amount,
            user_registration_date=user.created_at.strftime("%d.%m.%Y")
        ),
        reply_markup=keyboard
    )    
