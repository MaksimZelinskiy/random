import logging
from aiogram import Router, F
from aiogram.fsm.context import FSMContext  
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ChatMemberUpdated, Message, CallbackQuery
from aiogram.fsm.storage.base import StorageKey

from filters.check_reg import IsPrivate
from database.repo.requests import RequestsRepo
from loader import bot
from data.config import admins

logger = logging.getLogger(__name__)
router = Router()


EMOJI_STATUS_CHANNEL = {
    "active": "✅",
    "blocked": "🔴",
}


@router.callback_query(F.data == "add_channel")
async def add_channel(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    if await state.get_state() is not None:
        await state.clear()
    channels = await repo.channels.get_channels_by_admin_id(callback.from_user.id)

    bot_me = await bot.get_me()
    bot_link = f"https://t.me/{bot_me.username}"
    
    buttons = []
    buttons.append([InlineKeyboardButton(text="Добавить канал", url=f"{bot_link}?startchannel&admin=change_info+invite_users+restrict_members+post_messages")])
    for channel in channels:
        buttons.append([InlineKeyboardButton(text=f"{EMOJI_STATUS_CHANNEL[channel.channel_status]} {channel.channel_title}", callback_data=f"channel_view:{channel.id}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
     
    msg = await callback.message.edit_text("Мои каналы", reply_markup=keyboard)
    await state.update_data(giveaway_channels_message_id=msg.message_id)


@router.message(F.text == "🔗 Мои каналы", IsPrivate())
async def command_start(message: Message, repo: RequestsRepo, state: FSMContext):
    if await state.get_state() is not None:
        await state.clear()
        
    channels = await repo.channels.get_channels_by_admin_id(message.from_user.id)

    bot_me = await bot.get_me()
    bot_link = f"https://t.me/{bot_me.username}"
    
    buttons = []
    buttons.append([InlineKeyboardButton(text="Добавить канал", url=f"{bot_link}?startchannel&admin=change_info+invite_users+restrict_members+post_messages")])
    for channel in channels:
        buttons.append([InlineKeyboardButton(text=f"{EMOJI_STATUS_CHANNEL[channel.channel_status]} {channel.channel_title}", callback_data=f"channel_view:{channel.id}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    
    if not channels:
        msg = await message.answer("❌ У вас еще нет каналов", reply_markup=keyboard)
        await state.update_data(giveaway_channels_message_id=msg.message_id)
        return
     
    msg = await message.answer("Мои каналы", reply_markup=keyboard)
    await state.update_data(giveaway_channels_message_id=msg.message_id)


# способ добавления бота в канал администратором
@router.my_chat_member(F.new_chat_member.status.in_(["administrator", "member", "kicked", "restricted", "left"]))
async def bot_added_as_admin(event: ChatMemberUpdated, state: FSMContext, repo: RequestsRepo):
    added_by_user_id = event.from_user.id
    channel_id = event.chat.id
    channel_title = event.chat.title
    channel_username = event.chat.username
    channel_link = f"https://t.me/{channel_username}"
    
    key = StorageKey(user_id=added_by_user_id, chat_id=added_by_user_id, bot_id=bot.id)
    state_user = FSMContext(storage=state.storage, key=key)

    data = await state_user.get_data()        
    msg_id = data.get("giveaway_channels_message_id")
    try:
        await bot.delete_message(added_by_user_id, msg_id)
    except Exception as e:
        logger.error(f"Ошибка при удалении сообщения: {e}")
    
    bot_me = await bot.get_me()
    bot_link = f"https://t.me/{bot_me.username}"
        
    if channel_username == None:
        await bot.send_message(added_by_user_id, "🔴 Бот не может добавить этот канал, так как он закрыт.")  
        return 
    
    if event.new_chat_member.status == "administrator":
        
        get_channel = await repo.channels.get_channel_by_id(str(channel_id))
        if get_channel:
            await repo.channels.delete_channel(str(channel_id))

        logger.info(f"Бот был добавлен как админ в канал: {channel_id} ({channel_title})")
        
        await repo.channels.bind_channel_to_admin(added_by_user_id, str(channel_id), channel_title, channel_username, channel_link)  
        await repo.commit()

        channels = await repo.channels.get_channels_by_admin_id(added_by_user_id)
        
        buttons = []
        buttons.append([InlineKeyboardButton(text="Добавить канал", url=f"{bot_link}?startchannel&admin=change_info+invite_users+restrict_members+post_messages")] )
        for channel in channels:
            buttons.append([InlineKeyboardButton(text=f"{EMOJI_STATUS_CHANNEL[channel.channel_status]} {channel.channel_title}", callback_data=f"channel_view:{channel.id}")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        msg = await bot.send_message(added_by_user_id, f"✅ Бот был успешно добавлен в канал: {channel_title}\n\nЧтобы добавить ещё канал, нажмите на кнопку выше", reply_markup=keyboard)
        await state_user.update_data(giveaway_channels_message_id=msg.message_id)

    elif event.new_chat_member.status in  ["kicked", "restricted", "left"]:
        logger.info(f"Бот был удален из канала: {channel_id} ({channel_title})")
        
        await repo.channels.update_status_channel(added_by_user_id, str(channel_id), "blocked")
        
        await repo.commit()
        
        channels = await repo.channels.get_channels_by_admin_id(added_by_user_id)
        
        buttons = []
        buttons.append([InlineKeyboardButton(text="Добавить канал", url=f"{bot_link}?startchannel&admin=change_info+invite_users+restrict_members+post_messages")])
        for channel in channels:
            buttons.append([InlineKeyboardButton(text=f"{EMOJI_STATUS_CHANNEL[channel.channel_status]} {channel.channel_title}", callback_data=f"channel_view:{channel.id}")])
        
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        
        msg = await bot.send_message(added_by_user_id, f"🔴 Бот был удален из канала: {channel_title}\n\nЧтобы добавить ещё канал, нажмите на кнопку выше", reply_markup=keyboard)
        await state_user.update_data(giveaway_channels_message_id=msg.message_id)


@router.callback_query(F.data.startswith("channel_view:"), IsPrivate())
async def channel_view(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    channel_id = callback.data.split(":")[1]
    channel = await repo.channels.get_channel_by_id(channel_id)
    await callback.message.answer(f"🔗 Канал: {channel.channel_title}\n\n🔗 Ссылка: {channel.channel_link}")

