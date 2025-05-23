import asyncio
from datetime import datetime
import logging
import os 

from aiogram import Router, F, types

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardMarkup, KeyboardButton, FSInputFile   
from aiogram.filters import Command, CommandObject, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate
from loader import bot
from tg_utils import texts, keyboards
from database.repo.requests import RequestsRepo
from database.models.offers import OFFER_STATUS_SYMBOLS, OFFER_STATUS_TEXTS
from utils import message as message_utils 

from data import config

from loader import bot
    
logger = logging.getLogger(__name__)
router = Router()

class BalanceAdd(StatesGroup):
    amount = State()
    photo = State()

@router.callback_query(F.data == "deposit")
async def balance_add(callback: CallbackQuery, repo: RequestsRepo, state: FSMContext):
    user = await repo.users.get_user_if_exists(callback.from_user.id)
    
    if not user:
        await callback.answer("Вы не авторизованы")
        return
    
    currency = 'usdt'
    
    await state.update_data(currency=currency)
    
    keyboard = await keyboards.BalanceKeyboard().amount(currency)
    await message_utils.send_message(
        callback.message, 
        texts.BALANCE[
            "amount_currency"
        ].format(
            currency=currency, 
            min_amount=config.MIN_AMOUNT_ADD[currency]
        ),
        reply_markup=keyboard
    )
    await state.set_state(BalanceAdd.amount)    
    
@router.message(StateFilter(BalanceAdd.amount))
async def balance_add_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите целое число")
        return
    
    await state.update_data(amount=int(message.text))
    
    data = await state.get_data()
    currency = data.get("currency")
    amount = data.get("amount")
    
    text = (
        "Отправьте с любого кошелька на наш адрес\n"
        "❕Заявка для вашей суммы активна 30 минут\n"
        "USDT TRC20:\n"
        f"<code>{config.WALLET[currency]}</code>\n\n"
        "❗️<b>Сумма для пополнения: (обязательно)</b>\n"
        f"<code>{amount}</code>\n\n"
        "📝 <b>Инструкция по оплате:</b>\n"
        "1. Переведите указанную сумму на кошелек\n"
        "2. Сделайте скриншот успешной транзакции \n"
        "3. Отправьте скриншот боту для подтверждения\n\n"
        "❗️ Оплата будет проверена администратором в течение 24 часов"
    )
    
    await message.answer(text, parse_mode="HTML")
    await state.set_state(BalanceAdd.photo)
    
@router.message(StateFilter(BalanceAdd.photo))
async def balance_add_photo(message: Message, state: FSMContext, repo: RequestsRepo):
    if message.content_type != "photo":
        await message.answer("Отправьте скриншот успешной транзакции")
        return
    
    await state.update_data(photo=message.photo)
    
    data = await state.get_data()
    currency = data.get("currency")
    amount = data.get("amount")

    await state.clear()
    
    # Создание заявки на пополнение баланса
    await repo.balance.create_balance_request(
        user_id=message.from_user.id,
        amount=int(amount),
        currency=currency
    )
    
    keyboard = await keyboards.ModerationKeyboard().balance_add(
        user_id=message.from_user.id,
        amount=amount,
        currency=currency
    )
    
    user_link = f"https://t.me/{message.from_user.username}" if message.from_user.username else "tg://user?id=" + str(message.from_user.id)
    
    await bot.send_photo(
        config.CHATS['moderation']['chat_id'],
        message_thread_id=config.CHATS['moderation']['topics']['money'],
        photo=message.photo[-1].file_id,
        caption=texts.BALANCE["moderation"]["add"].format(
            user_id=message.from_user.id,
            user_name=message.from_user.first_name,
            user_username=message.from_user.username,
            amount=amount,
            user_link=user_link,
            currency=currency,
            wallet=config.WALLET[currency],
            date=datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )
    
    keyboard = await keyboards.main_menu_keyboard()
    await message.answer(
        (
            "<b>Ваша заявка на пополнение баланса успешно принята</b>\n\n"
            "Ожидай подтверждения администратором."
        ),
        reply_markup=keyboard
    )
    