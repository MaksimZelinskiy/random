from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

async def main_menu_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,   
        keyboard=[
            [KeyboardButton(text=f"🎁 Создать розыгрыш")],
            [KeyboardButton(text="📊 Мои розыгрыши")],
            [KeyboardButton(text="🔗 Мои каналы")],
            [KeyboardButton(text="� Админ-панель")]
        ]
    )
    
async def cancel_keyboard() -> InlineKeyboardMarkup:
    return ReplyKeyboardMarkup(
        resize_keyboard=True,   
        keyboard=[
            [KeyboardButton(text="Отмена")]
        ]
    )
    
    