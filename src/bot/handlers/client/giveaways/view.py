import asyncio
from datetime import datetime, timedelta
import logging
import os 

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardMarkup, KeyboardButton, FSInputFile   
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.types import ChatMemberUpdated

from filters import IsPrivate
from loader import bot
from data import config
from database.repo.requests import RequestsRepo
from utils import keyboards, texts

from clients.giveaway import send_giveaway_message

logger = logging.getLogger(__name__)

router = Router()

EMOJI_STATUS = {
    "active": "🟢",
    "block": "🔴",
    "wait_start": "⏳",
    "winners_selection": "🏆",
    "finished": "✅"
}

TEXT_STATUS = {
    "active": "🟢 Активный",
    "block": "🔴 Блокирован",
    "wait_start": "⏳ Ожидает начала",
    "winners_selection": "🏆 Выбор победителей",
    "finished": "✅ Завершен"
}

@router.message(F.text == "📊 Мои розыгрыши", IsPrivate())
async def command_start(message: Message, repo: RequestsRepo, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
        
    giveaways = await repo.giveaways.get_giveaways_by_admin_id(message.from_user.id)
    
    if not giveaways:
        await message.answer("🎁 У вас еще нет розыгрышей")
        return

    buttons = []
    for giveaway in giveaways:
        buttons.append([InlineKeyboardButton(text=f"{EMOJI_STATUS[giveaway.status]} {giveaway.id}", callback_data=f"giveaway_view:{giveaway.id}")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("🎁 Мои розыгрыши", reply_markup=keyboard)
    

@router.callback_query(F.data.startswith("giveaway_view:"), IsPrivate())        
async def giveaway_view(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):        
    giveaway_id = callback.data.split(":")[1]
    giveaway = await repo.giveaways.get_giveaway_by_id_and_admin_id(giveaway_id, callback.from_user.id)
    
    if not giveaway:
        await callback.answer("🎁 Розыгрыш не найден")
        return
    
    await send_giveaway_message(giveaway, callback.from_user.id)
    
    keyboard = InlineKeyboardMarkup()
    buttons = []
    
    if giveaway.status == "active":
        buttons.append([InlineKeyboardButton(text="Перейти к розыгрышу", url=f"{giveaway.view_details.get('url_to_giveaway')}")])
        buttons.append([InlineKeyboardButton(text="Изменить условие", callback_data=f"giveaway_edit_condition:{giveaway.id}")])
    elif giveaway.status == "wait_start":
        buttons.append([InlineKeyboardButton(text="Изменить условие", callback_data=f"giveaway_edit_condition:{giveaway.id}")])
    else:
        buttons.append([InlineKeyboardButton(text="Выгрузить таблицу участников", callback_data=f"giveaway_export_participants:{giveaway.id}")])
        buttons.append([InlineKeyboardButton(text="Выбрать дополнительных победителей", callback_data=f"giveaway_select_winners:{giveaway.id}")])

    buttons.append([InlineKeyboardButton(text="Удалить розыгрыш", callback_data=f"giveaway_delete:{giveaway.id}")])
    
    await callback.message.answer(f"🎁 <b>Розыгрыш #{giveaway.id}</b>\n\n"
                                  f"🔹 Статус: {TEXT_STATUS[giveaway.status]}\n"
                                  f"🔹 Начало: {giveaway.start_at}\n"
                                  f"🔹 Окончание: {giveaway.ends_at}\n"
                                  f"🔹 Количество победителей: {giveaway.count_winners}\n"
                                  f"🔹 Количество участников: {giveaway.count_participants}\n", reply_markup=keyboard)
    