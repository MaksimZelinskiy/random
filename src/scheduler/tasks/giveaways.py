import asyncio
from datetime import datetime
from config import logging
from database.repo.requests import RequestsRepo
from database.setup import get_session_pool

import random
import time
from aiogram.exceptions import TelegramForbiddenError
from database.models.giveaways import Giveaway
from utils_system.tg import TG_BOT

logger = logging.getLogger(__name__)

async def giveaway_results_tick():
    session = get_session_pool()
    async with session() as session:
        try:
            repo = RequestsRepo(session)
            giveaways = await repo.giveaways.get_ready_giveaway_results()
            
            for giveaway in giveaways:
                await create_and_schedule_result_message(giveaway, repo)
            
            logger.info("Giveaway results tick")
        
        except Exception as e:
            logger.exception(f"Ошибка при создании итогов розыгрыша: {e}")


async def check_subscribed(bot, user_id: int, channel_ids: list[int]) -> tuple[bool, int]:
    try:
        for channel_id in channel_ids:
            member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False, user_id
        return True, user_id

    except TelegramForbiddenError as e:
        logging.warning(f"❌ Бот не имеет прав на канал {channel_ids}: {e}")
        return True, user_id

    except Exception as e:
        logging.exception(f"🔥 Непредвиденная ошибка: user_id={user_id}, error={e}")
        return True, user_id

async def create_and_schedule_result_message(giveaway: Giveaway, repo: RequestsRepo):

    # 1. Все участники розыгрыша
    participants = await repo.giveaways.get_participants(giveaway.id) 
    # 2. Обязательные каналы
    required_channel_ids = giveaway.required_channels

    winners = []
    l_tasks_winner_add = [] 
    place = 1        
    while len(winners) < giveaway.count_winners:
        random.shuffle(participants)  # случайный порядок

        l_tasks = []
        # ПРОВЕРЯЕМ ТОЛЬКО НУЖНЫХ
        for user in participants[:giveaway.count_winners - len(winners)]:
            l_tasks.append(check_subscribed(user.telegram_id, required_channel_ids))

        results = await asyncio.gather(*l_tasks)
        for result in results:
            user_id = result[1]
            status = result[0]
            
            if status:
                winners.append({
                    "user_id": user_id,
                    "place": place
                })
                l_tasks_winner_add.append(repo.giveaways.add_giveaway_winner(giveaway.id, user_id, place, "main"))
                place += 1

    if not winners:
        logger.warning(f"Не удалось выбрать победителей для розыгрыша {giveaway.id}")
        return
    
    # Обновляем статус розыгрыша
    await repo.giveaways.update_giveaway_status(giveaway.id, "finished")
    # Добавляем победителей в розыгрыш
    await asyncio.gather(*l_tasks_winner_add)
    
    await repo.commit()
    
    l_users = await repo.users.get_users_by_ids(winners)
    user_map = {u.user_id: u for u in l_users}    
    
    # 4. Создаём итоговый пост
    TEXT = f"<b>Розыгрыш #{giveaway.id} завершен</b>\n\n"
    TEXT += "<b>Победители:</b>\n"

    for place, user_id in enumerate(winners, start=1):
        user = user_map.get(int(user_id))
        if user:
            TEXT += f"{place}. <a href='tg://user?id={user.user_id}'>{user.name}</a>\n"
    
    for channel in giveaway.publish_channels:
        await repo.mailings.create_mailing(
            created_by_admin_id=giveaway.admin_id,
            task_type="giveaway",
            target_id=channel,
            message_type="text",
            media_file_id=None,
            text=TEXT,
            reply_markup=None,
            scheduled_at=datetime.now()
        )
    
    await repo.commit()


