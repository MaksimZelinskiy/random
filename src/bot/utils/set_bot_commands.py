from aiogram import types, Dispatcher

from loader import bot

async def set_defualt_commands(dp: Dispatcher):
    # await dp.bot.set_chat_menu_button(
    #         menu_button=types.MenuButtonWebApp(text="Играть", web_app=types.WebAppInfo(url=f"https://app.dreamcoin.pro/"))
    #     )    
    await bot.set_my_commands([
        types.BotCommand(command='start', description='Start'),
    ])
    pass