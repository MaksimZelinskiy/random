from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link

from loader import bot
from data.config import admins
from database.repo.requests import RequestsRepo

router = Router()


async def check_all_users(repo: RequestsRepo):
    users = await repo.users.get_users_by_status_and_filters()
    
    for user in users:
        try:
            await bot.send_chat_action(user.user_id, "typing")
        except:
            await repo.users.update_user_status(user.user_id, "blocked")


@router.callback_query(F.data == "user_stat") 
async def users_stat(callback: CallbackQuery, repo: RequestsRepo):
    active_users = len(await repo.users.get_users_by_status("active")) 
    blocked_users = len(await repo.users.get_users_by_status("blocked"))
    all_users = active_users + blocked_users

    stats = await repo.users.get_detailed_stats_utm_codes()
    print(stats)
    ref_stats = "<b>Статистика по UTM-меткам</b>\n\n" + '\n\n'.join([
        f"""<b>{referrer_id}</b>:\nВсего: {count_users} пользователей"""
        for count_users, referrer_id in stats
    ]) + "\n\n"


    lang_stats = await repo.users.get_language_stats()
    lang_text = "<b>Статистика по языкам пользователей:</b>\n" + "\n".join(
        [f"{lang or 'Не указан'}: {count}" for lang, count in lang_stats]
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Обновить", callback_data="reload_stats")]
    ])

    ref_link = await create_start_link(bot, "link_name")
    hints = f'ℹ️ <i>Подсказки:</i>\n- Создание реферальной ссылки: \n<code>{ref_link}</code>\n\n- Кнопка «Обновить»:\nОбновляет статусы пользователей.'

    recent_stats = await repo.users.get_recent_stats(5)
    recent_logins = await repo.user_login.get_recent_stats_logins(5)
    recent_logins_today = recent_logins[0][1] if recent_logins else 0
    recent_stats_today = recent_stats[0][1] if recent_stats else 0

    general_stats = f"""
<b>Общая:</b>
Всего пользователей: {active_users + blocked_users}/{active_users} ({all_users})

<b>Подробно за сегодня:</b>
Онлайн: {recent_logins_today}
Новых: {recent_stats_today}"""

    stats_text = "\n".join([
        f"{reg[0].strftime('%d.%m.%Y')}:  +{reg[1]}  |  {log[1]}"
        for reg, log in zip(recent_stats, recent_logins)
    ])

    full_text = f"<b>СТАТИСТИКА</b>:\n\n{general_stats}\n\n{stats_text}\n\n<i>Дата:      +Новых  |  Онлайн</i>\n"

    await callback.message.answer(full_text)
    await callback.message.answer(ref_stats)
    await callback.message.answer(lang_text)
    await callback.message.answer(hints, reply_markup=kb)
    
    return True
