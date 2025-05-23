from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery
import logging

from loader import bot
from tg_utils import texts, keyboards

logger = logging.getLogger(__name__)

async def send_message(
    message: Message | CallbackQuery, 
    text: str, 
    reply_markup: InlineKeyboardMarkup | None = None
) -> Message:
    """
    Universal function to handle all message sending cases in aiogram3.
    Tries to edit the message first, then falls back to sending a new message.
    Works with both Message objects and CallbackQuery objects.
    """
    try:
        # Check if message is from a callback query (has message attribute)
        if hasattr(message, 'message') and message.message:
            return await message.message.edit_text(text, reply_markup=reply_markup, disable_web_page_preview=True)
        
        # Try to edit existing message
        return await message.edit_text(text, reply_markup=reply_markup, disable_web_page_preview=True)
    except Exception as e:
        logger.debug(f"Could not edit message, trying to send new one: {e}")
        try:
            # If message is from callback query, use its message
            if hasattr(message, 'message') and message.message:
                return await message.message.answer(text, reply_markup=reply_markup, disable_web_page_preview=True)
                
             
            # Send as a new message
            return await message.answer(text, reply_markup=reply_markup, disable_web_page_preview=True)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")


async def main_menu(message: Message):
    keyboard = await keyboards.main_menu_keyboard()
    await bot.send_message(message.from_user.id, "<b>Главное меню</b>", reply_markup=keyboard, parse_mode="HTML")
    