import asyncio
from datetime import datetime
from typing import List
from tasks.base import send_message_by_type_to_user
from limiter import MAX_MESSAGES_PER_SECOND
from config import logging
from database import RequestsRepo
from database.setup import get_session_pool

TASK_PRIORITY = {
    'publication': 2, 'results': 1, 'mailing': 3
}

logger = logging.getLogger(__name__)    


async def mailing_tick():
    
    Session = get_session_pool()
    async with Session() as session:
        repo = RequestsRepo(session)
    
        now = datetime.utcnow()
        to_send: List = []

        try:
            # Получаем задачи для отправки в текущий тик 
            # ПЕРЕДАЕМ ТОЛЬКО ПРИОРИТЕТНЫЕ ЗАДАЧИ
            scheduled_tasks: List = await repo.mailings.get_mailings_by_datetime(now, limit=MAX_MESSAGES_PER_SECOND, task_types=["giveaway"])
            logger.info(f"Получено {len(scheduled_tasks)} задач для публикации")
            to_send.extend(scheduled_tasks)

            # Получаем количество задач для отправки
            used_slots = len(to_send)

            # Получаем количество оставшихся ячеек для задач
            remaining_slots = MAX_MESSAGES_PER_SECOND - used_slots

            # Если есть оставшиеся ячейки, то получаем задачи для рассылки
            if remaining_slots > 0:
                # Получаем задачи для рассылки  
                # ПЕРЕДАЕМ ОСТАЛЬНЫЕ ЗАДАЧИ 
                mailing_tasks: List = await repo.mailings.get_mailings_by_datetime(now, limit=remaining_slots, task_types=["mailing"])

                # Добавляем задачи для рассылки в список
                to_send.extend(mailing_tasks)

            # Если нет задач для выполнения, то выходим
            if not to_send:
                logger.debug("Нет задач для выполнения в этом тике рассылки.")
                return

            # Сортируем задачи по приоритету и времени создания
            to_send.sort(key=lambda m: (TASK_PRIORITY.get(m.task_type, 99), m.created_at))

            l_tasks_mailings = []
            for mailing in to_send:
                # Добавляем задачу на выполнение отправки
                l_tasks_mailings.append(send_message_by_type_to_user(mailing))
            
            # Запуск задач на выполнение
            results = await asyncio.gather(*l_tasks_mailings)
            
            tasks_to_update = []
            # Обрабатываем результаты отправки
            for result in results:
                try:
                    status = "sent" if result[0] else "error"
                    msg_id = result[1].message_id if result[0] else None
                    user_mailing_data = result[2]
                    error_message = result[3]
                    
                    # Добавляем задачу на обновление статуса рассылки
                    tasks_to_update.append(
                        repo.mailings.update_mailing_status(
                            user_mailing_data, status, error_message, msg_id if msg_id else None
                        )
                    )    
                except Exception as e:
                    logger.exception(f"Ошибка при обновлении статуса рассылки: {e}")
                    
                    # Добавляем задачу на обновление статуса рассылки (если не удалось добавить задачу на обновление статуса)
                    tasks_to_update.append(
                        repo.mailings.update_mailing_status(
                            user_mailing_data, "error", str(e), None
                        )
                    ) 
                    
            if tasks_to_update:
                # Отправляем задачи на обновление статуса рассылки
                await asyncio.gather(*tasks_to_update)
                await repo.commit()

        except Exception as e:
            logger.exception(f"Ошибка в рассылочном тике: {e}")
            await repo.rollback()

