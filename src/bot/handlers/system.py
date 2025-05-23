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
from utils import texts, keyboards
from data import config
from database.repo.requests import RequestsRepo

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == "pass")
async def pass_def(callback: CallbackQuery):
    await callback.answer("Раздел в разработке...")
    
@router.message(F.text == "Главное меню")
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("<b>Главное меню</b>", reply_markup=await keyboards.main_menu_keyboard())

    
    