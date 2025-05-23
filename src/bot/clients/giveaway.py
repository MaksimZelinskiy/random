

from database.models.giveaways import Giveaway

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton    

from loader import bot


async def send_giveaway_message(giveaway: Giveaway, user_id: int):
    text = giveaway.view_details.get("text")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=giveaway.view_details.get("button_text"), callback_data="pass")]
    ])
    
    if giveaway.view_details.get("media_type") == "text":
        await bot.send_message(user_id, text, reply_markup=keyboard, disable_web_page_preview=True)
    elif giveaway.view_details.get("media_type") == "photo":
        await bot.send_photo(user_id, giveaway.view_details.get("media"), caption=text, reply_markup=keyboard)
    elif giveaway.view_details.get("media_type") == "video":
        await bot.send_video(user_id, giveaway.view_details.get("media"), caption=text, reply_markup=keyboard)
    elif giveaway.view_details.get("media_type") == "animation":
        await bot.send_animation(user_id, giveaway.view_details.get("media"), caption=text, reply_markup=keyboard)
    
        
