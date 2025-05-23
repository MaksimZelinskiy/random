from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from data.config import admins

router = Router()

@router.message(Command("admin"))
async def admin(message: Message, state: FSMContext):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Рассылка', callback_data='mailing'),
            ],
            [
                InlineKeyboardButton(text='Статистика', callback_data='user_stat'),
            ]
        ]
    )
    if message.from_user.id in admins:
        await message.answer(
            f'Привет, {message.from_user.full_name}', 
            reply_markup=markup
        )

