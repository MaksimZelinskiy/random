import asyncio
from datetime import datetime
import logging
import os 

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardMarkup, KeyboardButton, FSInputFile   
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy

from filters import IsPrivate
from loader import bot
from data import config
from database.repo.requests import RequestsRepo
from utils import keyboards, texts

logger = logging.getLogger(__name__)

router = Router()

@router.message(CommandStart(), IsPrivate())
async def command_start(message: Message, command: CommandObject, repo: RequestsRepo, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
    
    
    
    # если нет события, то присваиваем ref_id
    utm = command.args or "search"

    username = message.from_user.username
    locale = message.from_user.language_code
    name = message.from_user.first_name.replace("'", "")
    
    user = await repo.users.get_user_if_exists(message.from_user.id)
    
    if utm == "search":
        keyboard = await keyboards.main_menu_keyboard()
        await message.answer("Приветствуем!\n\nНаш бот поможет Вам провести розыгрыш в канале.\n\nГотовы создать новый розыгрыш?", reply_markup=keyboard)
    else:
        # Капча на вход
        pass
    
    
    if not user:
        try:
            await repo.users.create_user(
                user_id=message.from_user.id,
                utm=utm,
                name=name,
                username=username,
                language=locale,
                referrer_id=utm
            )
            await repo.commit()

        except Exception as e:
            await repo.rollback()
            logger.error(e)
            
    else:
        if user.is_active == False:
            await repo.users.update_user_by_id(message.from_user.id, "is_active", True)
            await repo.commit()

    return True
