import asyncio
from datetime import datetime, timedelta
import logging
import os 

from aiogram import Router, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile, ReplyKeyboardMarkup, KeyboardButton, FSInputFile   
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.types import ChatMemberUpdated

from filters import IsPrivate
from loader import bot
from data import config
from database.repo.requests import RequestsRepo
from utils import keyboards, texts

logger = logging.getLogger(__name__)

router = Router()

class CreateGiveawayState(StatesGroup):
    giveaway_message = State()
    giveaway_button_text = State()
    
    giveaway_count_winners = State()
    giveaway_start_date = State()
    giveaway_end_date = State()
    
    giveaway_publish_channels = State()
    giveaway_required_channels = State()
    
    giveaway_use_boost = State()
    giveaway_use_capha = State()
    giveaway_use_block_twinks = State()
    
    giveaway_save = State()
    
@router.message(F.text == "Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    keyboard = await keyboards.main_menu_keyboard()
    await message.answer("Главное меню", reply_markup=keyboard)


@router.message(F.text == "🎁 Создать розыгрыш", IsPrivate())
async def command_start(message: Message, repo: RequestsRepo, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
        
        
    get_channels_admin = await repo.channels.get_active_channels_by_admin_id(message.from_user.id)
    if not get_channels_admin:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Добавить канал", callback_data="add_channel")]
        ])
        await message.answer("❌ У вас нет активных каналов, для создания розыгрыша, сначала создайте канал и добавьте бота в него", reply_markup=keyboard)
        return
    
    get_active_giveaways = await repo.giveaways.get_active_giveaways_by_admin_id(message.from_user.id)
    if len(get_active_giveaways) >= 5:
        await message.answer("❌ У вас уже есть максимальное количество активных розыгрышей (5/5).")
        return
        
    await state.set_state(CreateGiveawayState.giveaway_message)
    
    text = (
        f"<b>Создание розыгрыша:</b>\n\n"
        f"✉️ Отправьте текст для розыгрыша. Вы можете также отправить вместе с текстом 🖼 картинку, видео, GIF или Премиум🎆эмодзи, а так же пользоваться разметкой.\n\n"
        f"❗️ Вы можете использовать только 1 медиафайл.\n\n"
        f"Бот для проведения конкурсов полностью бесплатный, прозрачный и ему будет приятно, если в конкурсном посте Вы укажите на него ссылку, спасибо. @RandomGiveaway_Bot"
    )
    
    keyboard = await keyboards.cancel_keyboard()
    await message.answer(text, reply_markup=keyboard)


@router.message(StateFilter(CreateGiveawayState.giveaway_message), IsPrivate())
async def giveaway_message(message: Message, state: FSMContext):
    
    if message.content_type not in ["text", "photo", "video", "animation"]:
        await message.answer("🚫 Данный формат не поддерживается.")
        return
    
    await state.update_data(giveaway_message=message.html_text)
    
    if message.photo:
        await state.update_data(giveaway_media=message.photo[0].file_id)
        await state.update_data(giveaway_media_type="photo")
        
        await message.answer_photo(message.photo[0].file_id, caption=message.html_text)    
    elif message.video:
        await state.update_data(giveaway_media=message.video.file_id)
        await state.update_data(giveaway_media_type="video")
        
        await message.answer_video(message.video.file_id, caption=message.html_text)
    elif message.animation:
        await state.update_data(giveaway_media=message.animation.file_id)
        await state.update_data(giveaway_media_type="animation")
        
        await message.answer_animation(message.animation.file_id, caption=message.html_text)
    elif message.sticker:
        await state.update_data(giveaway_media=message.sticker.file_id)
        await state.update_data(giveaway_media_type="sticker")
        
        await message.answer_sticker(message.sticker.file_id, caption=message.html_text)
    else:
        await state.update_data(giveaway_media_type="text")
        await message.answer(message.html_text, disable_web_page_preview=True) 
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подтвердить", callback_data="giveaway_confirm_message")]
    ])
    await message.answer("Подтвердите сообщение для розыгрыша или отправьте другое сообщение.", reply_markup=keyboard)
    
    
@router.callback_query(F.data == "giveaway_confirm_message", StateFilter(CreateGiveawayState.giveaway_message))
async def giveaway_confirm_message(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("✅ Сообщение для розыгрыша подтверждено и сохранено.")
    await state.set_state(CreateGiveawayState.giveaway_button_text)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Участвовать", callback_data=f"giveaway_choose_text:Участвовать")],
        [InlineKeyboardButton(text="Участвую!", callback_data=f"giveaway_choose_text:Участвую!")],
        [InlineKeyboardButton(text="Принять участие", callback_data=f"giveaway_choose_text:Принять участие")]
    ])
    await callback.message.answer("✉️ Отправьте текст, который будет отображаться на кнопке, или выберите один из вариантов кнопкой:", reply_markup=keyboard)

    
@router.callback_query(F.data.startswith("giveaway_choose_text:"), StateFilter(CreateGiveawayState.giveaway_button_text))
async def giveaway_button_text(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):

    await state.update_data(giveaway_button_text=callback.data.split(":")[1])
    await callback.message.edit_text("✅ Текст кнопки сохранен")
    
    await state.set_state(CreateGiveawayState.giveaway_required_channels)
    
    channels = await repo.channels.get_channels_by_admin_id(callback.from_user.id)  
    
    await state.update_data(giveaway_required_channels=[])
    await state.update_data(user_channels=channels)
    
    buttons = []
    for channel in channels:
        buttons.append([InlineKeyboardButton(text=f"{channel.channel_title}", callback_data=f"gcrc:{channel.channel_id}:no")])
    buttons.append([InlineKeyboardButton(text="Готово", callback_data="giveaway_choose_channels_done")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    msg = await callback.message.answer("Выберите каналы, в которых будет проверяться подписка:", reply_markup=keyboard)
    await state.update_data(giveaway_channels_message_id=msg.message_id)

@router.callback_query(F.data.startswith("gcrc:"), StateFilter(CreateGiveawayState.giveaway_required_channels))
async def giveaway_choose_channel(callback: CallbackQuery, state: FSMContext):
    channel_id = callback.data.split(":")[1]
    is_checked = callback.data.split(":")[2]
    
    data = await state.get_data()
    user_channels = data.get("user_channels")
    giveaway_required_channels = data.get("giveaway_required_channels", [])
    
    if is_checked == "no":
        giveaway_required_channels.append(channel_id)
    else:
        giveaway_required_channels.remove(channel_id)
        
    await state.update_data(giveaway_required_channels=giveaway_required_channels)  
    
    buttons = []
    for channel in user_channels:
        if channel.channel_id in giveaway_required_channels:
            buttons.append([InlineKeyboardButton(text=f"{channel.channel_title} ✅", callback_data=f"gcrc:{channel.channel_id}:yes")])
        else:
            buttons.append([InlineKeyboardButton(text=f"{channel.channel_title}", callback_data=f"gcrc:{channel.channel_id}:no")])
    buttons.append([InlineKeyboardButton(text="Готово", callback_data="giveaway_choose_channels_done")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    
@router.callback_query(F.data == "giveaway_choose_channels_done", StateFilter(CreateGiveawayState.giveaway_required_channels))
async def giveaway_choose_channels_done(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text("🏆 Сколько победителей выбрать боту?")
    
    await state.set_state(CreateGiveawayState.giveaway_count_winners)
    
@router.message(StateFilter(CreateGiveawayState.giveaway_count_winners), IsPrivate())
async def giveaway_count_winners(message: Message, state: FSMContext, repo: RequestsRepo):
    try:
        count_winners = int(message.text)
        
        if count_winners <= 0:
            await message.answer("❌ Количество победителей должно быть больше 0")
            return
        elif count_winners > 250:
            await message.answer("❌ Количество победителей должно быть меньше 250")
            return
        
        await state.update_data(giveaway_count_winners=count_winners)
        await message.answer("✅ Количество победителей сохранено")
    
    except ValueError:
        await message.answer("❌ Количество победителей должно быть числом")
        return
    
    buttons = []
    channels = await repo.channels.get_channels_by_admin_id(message.from_user.id)
    for channel in channels:
        buttons.append([InlineKeyboardButton(text=channel.channel_title, callback_data=f"gcpc:{channel.channel_id}")])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    await message.answer("🗒 В каком канале публикуем розыгрыш?\n\nОн должен быть в <code>🔗 Мои каналы</code>.", reply_markup=keyboard)
    await state.set_state(CreateGiveawayState.giveaway_publish_channels)


@router.callback_query(F.data.startswith("gcpc:"), StateFilter(CreateGiveawayState.giveaway_publish_channels))
async def giveaway_choose_publish_channels(callback: CallbackQuery, state: FSMContext):
    channel_id = callback.data.split(":")[1]
    
    await state.update_data(giveaway_publish_channel_id=channel_id)
    await callback.message.edit_text("✅ Канал сохранен")

    await state.set_state(CreateGiveawayState.giveaway_start_date)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Прямо сейчас", callback_data="giveaway_choose_start_date:now")]
    ])
    
    date_now = datetime.now()
    text = (
        f"🕒 Введите дату начала розыгрыша в формате ДД.ММ.ГГГГ ЧЧ:ММ\n\n"
        f"<b>Примеры:</b>\n\n"
        f"<code>{(date_now + timedelta(minutes=10)).strftime('%d.%m.%Y %H:%M')}</code> - через 10 минут\n"
        f"<code>{(date_now + timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')}</code> - через час\n"
        f"<code>{(date_now + timedelta(days=1)).strftime('%d.%m.%Y %H:%M')}</code> - через день\n"
        f"<code>{(date_now + timedelta(days=7)).strftime('%d.%m.%Y %H:%M')}</code> - через неделю"
    )
    await callback.message.answer(text, reply_markup=keyboard)
    
@router.message(StateFilter(CreateGiveawayState.giveaway_start_date), IsPrivate())
async def giveaway_start_date(message: Message, state: FSMContext):
    date_str = message.text
    try:
        date_start = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("❌ Неверный формат даты")
        return
    
    await state.update_data(giveaway_start_date=date_start)
    date_now = datetime.now()   
    text = (
        f"🔚 Когда нужно определить победителя?\n\nУкажите время в формате ДД.ММ.ГГГГ ЧЧ:ММ\n\n"
        f"<b>Примеры:</b>\n\n"
        f"<code>{(date_now + timedelta(minutes=10)).strftime('%d.%m.%Y %H:%M')}</code> - через 10 минут\n"
        f"<code>{(date_now + timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')}</code> - через час\n"
        f"<code>{(date_now + timedelta(days=1)).strftime('%d.%m.%Y %H:%M')}</code> - через день\n"
        f"<code>{(date_now + timedelta(days=7)).strftime('%d.%m.%Y %H:%M')}</code> - через неделю\n\n"
        f"Бот живет по времени (GMT+3) Москва, Россия"
    )
    await message.answer(text)  
    await state.set_state(CreateGiveawayState.giveaway_end_date)

    
@router.callback_query(F.data.startswith("giveaway_choose_start_date:"), StateFilter(CreateGiveawayState.giveaway_start_date))
async def giveaway_choose_start_date(callback: CallbackQuery, state: FSMContext):
    date_str = callback.data.split(":")[1]
    if date_str == "now":
        date_start = datetime.now()
    else:
        date_start = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
        
    await state.update_data(giveaway_start_date=date_start)
    date_now = datetime.now()   
    text = (
        f"🔚 Когда нужно определить победителя?\n\nУкажите время в формате ДД.ММ.ГГГГ ЧЧ:ММ\n\n"
        f"<b>Примеры:</b>\n\n"
        f"<code>{(date_now + timedelta(minutes=10)).strftime('%d.%m.%Y %H:%M')}</code> - через 10 минут\n"
        f"<code>{(date_now + timedelta(hours=1)).strftime('%d.%m.%Y %H:%M')}</code> - через час\n"
        f"<code>{(date_now + timedelta(days=1)).strftime('%d.%m.%Y %H:%M')}</code> - через день\n"
        f"<code>{(date_now + timedelta(days=7)).strftime('%d.%m.%Y %H:%M')}</code> - через неделю\n\n"
        f"Бот живет по времени (GMT+3) Москва, Россия"
    )
    await callback.message.edit_text(text)  
    await state.set_state(CreateGiveawayState.giveaway_end_date)
    
    
@router.message(StateFilter(CreateGiveawayState.giveaway_end_date), IsPrivate())
async def giveaway_end_date(message: Message, state: FSMContext, repo: RequestsRepo):
    date_str = message.text
    try:
        date_end = datetime.strptime(date_str, "%d.%m.%Y %H:%M")
    except ValueError:
        await message.answer("❌ Неверный формат даты")
        return
    
    await state.update_data(giveaway_end_date=date_end)
    
    await message.answer("✅ Время для подведения результатов сохранено")  
    
    data = await state.get_data()
    giveaway_message = data.get("giveaway_message")
    giveaway_media = data.get("giveaway_media")
    giveaway_media_type = data.get("giveaway_media_type")
    
    giveaway_button_text = data.get("giveaway_button_text")
    giveaway_count_winners = data.get("giveaway_count_winners")
    
    giveaway_publish_channel_id = data.get("giveaway_publish_channel_id")   
    giveaway_required_channels = data.get("giveaway_required_channels")   
    
    giveaway_start_date = data.get("giveaway_start_date")
    giveaway_end_date = data.get("giveaway_end_date")
    
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=giveaway_button_text, callback_data="pass")]
    ])  
    
    text_giveaway = giveaway_message
    if giveaway_media_type == "photo":
        await message.answer_photo(giveaway_media, caption=text_giveaway, reply_markup=keyboard)
    elif giveaway_media_type == "video":
        await message.answer_video(giveaway_media, caption=text_giveaway, reply_markup=keyboard)
    elif giveaway_media_type == "animation":
        await message.answer_animation(giveaway_media, caption=text_giveaway, reply_markup=keyboard)
    elif giveaway_media_type == "sticker":
        await message.answer_sticker(giveaway_media, caption=text_giveaway, reply_markup=keyboard)
    elif giveaway_media_type == "text":
        await message.answer(text_giveaway, reply_markup=keyboard)
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сохранить", callback_data="giveaway_save")],
        [InlineKeyboardButton(text="Отменить", callback_data="giveaway_cancel")]
    ])
    
    channels_publish = await repo.channels.get_channels_by_ids([giveaway_publish_channel_id])
    channels_required = await repo.channels.get_channels_by_ids(giveaway_required_channels)
    
    text = (
        f"<b>Внимательно перепроверьте розыгрыш.</b>\n\n"
        f"Начало: {giveaway_start_date.strftime('%d.%m.%Y %H:%M')}\n"
        f"Конец: {giveaway_end_date.strftime('%d.%m.%Y %H:%M')}\n"
        f"Канал для публикации: {', '.join([f'<a href="{channel.channels_link}">{channel.channel_title}</a>' for channel in channels_publish])}\n"
        f"Канал(ы) для проверки: {', '.join([f'<a href="{channel.channels_link}">{channel.channel_title}</a>' for channel in channels_required])}\n\n"
        f"Количество победителей: {giveaway_count_winners}\n\n"
    )
    await message.answer(text, reply_markup=keyboard, disable_web_page_preview=True)
    
    await state.set_state(CreateGiveawayState.giveaway_save)
    
    
@router.callback_query(F.data.startswith("giveaway_"), StateFilter(CreateGiveawayState.giveaway_save))
async def giveaway_save(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    callback_data = callback.data.split("_")[1]
    
    if callback_data != "save":
        await callback.message.edit_text("❌ Розыгрыш не сохранен")
        await state.clear() 
        await callback.message.answer("Главное меню", reply_markup=await keyboards.main_menu_keyboard())
        return
    
    data = await state.get_data()
    
    giveaway_message = data.get("giveaway_message")
    giveaway_media = data.get("giveaway_media")
    giveaway_media_type = data.get("giveaway_media_type")
    
    giveaway_button_text = data.get("giveaway_button_text")
    
    giveaway_count_winners = data.get("giveaway_count_winners")
    
    giveaway_publish_channel_id = data.get("giveaway_publish_channel_id")   
    giveaway_required_channels = data.get("giveaway_required_channels")   
    
    giveaway_start_date = data.get("giveaway_start_date")
    giveaway_end_date = data.get("giveaway_end_date")
    try:
        
        await repo.giveaways.create_giveaway(   
            admin_id=callback.from_user.id,
            publish_channels=[giveaway_publish_channel_id],
            required_channels=giveaway_required_channels,
            view_details={
                "text": giveaway_message,
                "media": giveaway_media,
                "media_type": giveaway_media_type,
                "button_text": giveaway_button_text,
            },
            count_winners=giveaway_count_winners,
            use_boost=False,
            use_capha=False,
            use_block_twinks=False,
            start_at=giveaway_start_date,
            ends_at=giveaway_end_date,
        )
        await repo.mailings.create_mailing(
            created_by_admin_id=callback.from_user.id,
            task_type="giveaway",
            target_id=giveaway_publish_channel_id,
            message_type=giveaway_media_type,
            media_file_id=giveaway_media,
            text=giveaway_message,
            reply_markup=[{
                "text": giveaway_button_text,
                "url": "link_for_join_giveaway.com"
            }],
            scheduled_at=giveaway_start_date,
        )
        await repo.commit()
    
    except Exception as e:

        logger.error(f"Ошибка при создании розыгрыша: {e}")
        await callback.message.answer("❌ Розыгрыш не сохранен")
        await state.clear()
        return
    
    text_publish = " в течение 10 минут" if giveaway_start_date < datetime.now() else f": {giveaway_start_date.strftime('%d.%m.%Y %H:%M')}"
    
    await callback.message.edit_text("✅ Розыгрыш сохранен\n\n"
                                  f"🔔 Будет опубликован{text_publish}")
    await state.clear()
    