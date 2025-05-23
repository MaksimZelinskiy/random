import asyncio
import time
from typing import Dict, List, Tuple, Any

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.exceptions import TelegramRetryAfter

from loader import bot
from data.config import admins
from database.repo.requests import RequestsRepo

router = Router()

class CustomMailing(StatesGroup):
    data_mailing = State()
    add_data_mailing = State() 
    add_data_mailing_button_text = State()
    add_data_mailing_button_url = State()
    start_mailing = State()

@router.callback_query(F.data == "admin_panel")
async def mailing_start_main(callback: CallbackQuery, state: FSMContext):
    await state.clear()

@router.callback_query(F.data == "mailing")
async def mailing_start(callback: CallbackQuery, repo: RequestsRepo, state: FSMContext):
    await state.set_state(CustomMailing.add_data_mailing)
    
    users = await repo.users.get_users_by_status(status="active")
    users_list = [[user.user_id, user.name] for user in users]
    await state.update_data(list_users=users_list)

    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Назад", callback_data="admin_panel")
    ]])
    await callback.message.edit_text("Отправьте сообщение", reply_markup=kb)

async def get_mailing_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Сбросить", callback_data="reset_data_mailing_message"),
            InlineKeyboardButton(text="Кнопка", callback_data="add_mailing_button")
        ],
        [
            InlineKeyboardButton(text="Готово", callback_data="accept_mailing_data"),
            InlineKeyboardButton(text="Выход", callback_data="admin_panel")
        ]
    ])

@router.message(CustomMailing.add_data_mailing, F.content_type.in_({
    "text", "photo", "animation", "video", "audio", 
    "voice", "document", "sticker", "video_note"
}))
async def handle_mailing_content(message: Message, state: FSMContext):
    data = await state.get_data()
    dict_type_message = data.get('dict_type_message', {
        "text": "",
        "media_status": False,
        "media": {
            "type_media": "",
            "file_id": ""
        },
        "button_status": False,
        "button": {
            "button_text": "",
            "button_url": ""
        }
    })

    if message.content_type == "text":
        dict_type_message["text"] = message.html_text
    else:
        await save_media_content(message, dict_type_message)

    await state.update_data(dict_type_message=dict_type_message)
    await send_message_mailing(message.from_user.id, message.from_user.first_name, dict_type_message)
    await message.answer(
        "Сообщение успешно сохранено для рассылки", 
        reply_markup=await get_mailing_keyboard()
    )

async def save_media_content(message: Message, dict_type_message: Dict):
    media_types = {
        "photo": lambda m: m.photo[-1].file_id,
        "animation": lambda m: m.animation.file_id,
        "video": lambda m: m.video.file_id,
        "audio": lambda m: m.audio.file_id,
        "voice": lambda m: m.voice.file_id,
        "document": lambda m: m.document.file_id,
        "sticker": lambda m: m.sticker.file_id,
        "video_note": lambda m: m.video_note.file_id
    }

    content_type = message.content_type
    file_id = media_types[content_type](message)

    dict_type_message["media_status"] = True
    dict_type_message["media"] = {
        "type_media": content_type,
        "file_id": file_id
    }
    
    if message.caption:
        dict_type_message["text"] = message.html_text

@router.callback_query(F.data == "add_mailing_button", CustomMailing.add_data_mailing)
async def add_mailing_button_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CustomMailing.add_data_mailing_button_text)
    await callback.message.answer("Введите название кнопки и ссылку в формате: Название кнопки - Ссылка кнопки")

@router.message(CustomMailing.add_data_mailing_button_text)
async def save_button_text_and_url(message: Message, state: FSMContext):
    try:
        button_text, button_url = map(str.strip, message.text.split("-", 1))
        
        data = await state.get_data()
        dict_type_message = data.get("dict_type_message", {})
        dict_type_message["button_status"] = True
        dict_type_message["button"] = {
            "button_text": button_text,
            "button_url": button_url
        }
        
        await state.update_data(dict_type_message=dict_type_message)
        await state.set_state(CustomMailing.add_data_mailing)

        await send_message_mailing(message.from_user.id, message.from_user.first_name, dict_type_message)
        await message.answer(
            f"Кнопка сохранена:\nНазвание: {button_text}\nСсылка: {button_url}",
            reply_markup=await get_mailing_keyboard()
        )

    except ValueError:
        await message.answer("Неверный формат. Пожалуйста, введите в формате: Название кнопки - Ссылка кнопки")

@router.callback_query(F.data == "accept_mailing_data", CustomMailing.add_data_mailing) 
async def accept_mailing_prompt(callback: CallbackQuery):
    await callback.message.delete()
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Да", callback_data="accept_mailing_data_yes"),
        InlineKeyboardButton(text="Нет", callback_data="accept_mailing_data_no")
    ]])
    await callback.message.answer("Вы уверены что хотите запустить рассылку?", reply_markup=kb)

@router.callback_query(F.data.startswith("accept_mailing_data_"), CustomMailing.add_data_mailing)
async def process_mailing(callback: CallbackQuery, repo: RequestsRepo, state: FSMContext):
    await callback.message.delete()
    
    if callback.data == "accept_mailing_data_yes":
        data = await state.get_data()
        dict_type_message = data.get("dict_type_message")
        list_users = data.get("list_users")
        
        await state.clear()
        start_time = time.time()

        await callback.message.answer(f"Начинаем рассылку для {len(list_users)} пользователей.")
        count_sent, mailing_id = await start_mailing(repo, list_users, dict_type_message, callback)

        end_time = time.time()
        time_sec = end_time - start_time
        
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Удалить рассылку", callback_data=f"delete_mailing_{mailing_id}")
            ]
        ])

        await callback.message.answer(
            f"Рассылка завершена. Успешно отправлено: {count_sent} сообщений.\n"
            f"Длительность: {time_sec/60:.2f} мин ({time_sec:.2f} sec)",
            reply_markup=kb
        )

    
    else:
        await state.clear()
        await callback.message.answer("Рассылка отменена.")

@router.callback_query(F.data.startswith("delete_mailing_"))
async def delete_mailing(callback: CallbackQuery, repo: RequestsRepo):
    mailing_id = callback.data.split("_")[2]
    # получаем все сообщения рассылки 
    # запуск цикла удаления рассылки 

    await callback.message.answer("В разработке...")


async def send_message_mailing(user_id: int, name: str, dict_type_message: Dict[str, Any]):
    text = str(dict_type_message["text"].replace("%name%", name)) if dict_type_message["text"] != "" else None

    
    markup = None
    if dict_type_message["button_status"]:
        markup = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(
                text=dict_type_message["button"]["button_text"], 
                url=dict_type_message["button"]["button_url"] if dict_type_message["button"]["button_url"].startswith("http") else None,
                callback_data=dict_type_message["button"]["button_url"] if not dict_type_message["button"]["button_url"].startswith("http") else None
            )
        ]])
    
    if dict_type_message["media_status"]:
        file_id = dict_type_message["media"]["file_id"]
        type_media = dict_type_message["media"]["type_media"]
        
        media_senders = {
            "photo": bot.send_photo,
            "animation": bot.send_animation,
            "video": bot.send_video,
            "document": bot.send_document,
            "audio": bot.send_audio,
            "voice": bot.send_voice,
            "video_note": bot.send_video_note,
            "sticker": bot.send_sticker
        }
        return await media_senders[type_media](user_id, file_id, caption=text, reply_markup=markup)
    
    else:
        return await bot.send_message(
            user_id, 
            text=str(text), 
            reply_markup=markup, 
            disable_web_page_preview=True
        )
        
async def send_message(user: List, dict_type_message: Dict):
    user_id, name = user
    try:
        message = await send_message_mailing(user_id, name, dict_type_message)
        return message
    except TelegramRetryAfter as e:
        await asyncio.sleep(e.retry_after)
        return await send_message(user, dict_type_message)
    except Exception as e:
        print(f"Failed to send message to {user_id}: {e}")
        return None

async def send_messages(repo: RequestsRepo, users: List[List], dict_type_message: Dict, mailing_id: int) -> int:
    tasks = [send_message(user, dict_type_message) for user in users]
    messages = await asyncio.gather(*tasks)

    tasks_messages = [
        repo.user_mailing.track_user_mailing(
            message.from_user.id, 
            mailing_id, 
            {
                "message_id": message.message_id,
                "message": message.model_dump()
            }

        ) for message in messages if message is not None
    ]
    await asyncio.gather(*tasks_messages)
    
    await repo.commit()
    return sum(1 for m in messages if m is not None)


from datetime import datetime

async def start_mailing(repo: RequestsRepo, list_users: List[List], dict_type_message: Dict, callback: CallbackQuery) -> int:

    if not list_users:
        return 0
    
    # list_users = list_users[:1000]
    
    progress_bar = {
        "all": len(list_users),
        "current": 0,
        "progress_in_percent": 0
    }

    def update_progress_bar(current: int):
        progress_bar["current"] = current
        progress_bar["progress_in_percent"] = round(progress_bar["current"] / progress_bar["all"] * 100)

    def get_progress_bar():
        progress = progress_bar["progress_in_percent"] // 10
        if progress_bar["progress_in_percent"] == 0:
            return "🟩" + "⬜️" * 9 + f" {progress_bar['progress_in_percent']}%"
        elif progress_bar["progress_in_percent"] == 100:
            return "🟩" * 10 + f" {progress_bar['progress_in_percent']}%"
        else:
            return "🟩" * (progress + 1) + "⬜️" * (9 - progress) + f" {progress_bar['progress_in_percent']}%"
            
    def get_text():
        now = datetime.now().strftime("%H:%M %d.%m.%Y")
        return (
            f"<b>Данные рассылки:</b>\n"
            f"<b>├ Количество пользователей:</b> {progress_bar['all']}\n"
            f"<b>├ Отправленных:</b> {progress_bar['current']}\n" 
            f"<b>└ Осталось:</b> {progress_bar['all'] - progress_bar['current']}\n\n"
            f"<b>Прогресс:</b> \n{get_progress_bar()}\n\n"
            f"<b>Админ:</b> @{callback.from_user.username}\n"
            f"<b>Началась:</b> {now}"
        )
    
    msgs = []
    for admin in admins:
        try:
            await send_message([admin, "admin"], dict_type_message)

            msgs.append(await bot.send_message(
                admin,
                get_text(),
                disable_web_page_preview=True
            ))

        except:
            pass
    
    count_batch = 30
    user_batches = [list_users[i:i + count_batch] for i in range(0, len(list_users), count_batch)]
    total_sent = 0
    total_all = 0
    start_time = time.time()

    for user_batch in user_batches:
        total_all += len(user_batch)
        total_sent += await send_messages(user_batch, dict_type_message)
        
        print(f"Sent: {total_sent}, Time: {time.time() - start_time:.2f}s")

        update_progress_bar(total_all)
        try:
            for msg in msgs:

                await msg.edit_text(
                    get_text(),
                    disable_web_page_preview=True
                )
        except Exception as e:
            print(f"Failed to update progress message: {e}")
        
        await asyncio.sleep(1)

    return total_sent