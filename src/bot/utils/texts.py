MAIN_MENU = """
<b>BoostMedia</b> — сервис нативного продвижения в Instagram.

У нас есть 2 способа использования:

<b>Для рекламодателей:</b> 
● Выбирайте пост (новый или существующий), который хотите продвинуть.
● Пишите 3–5 кликабельных комментариев — их будут использовать админы в своих Reels.
● Отправляйте заявку прямо в боте для запуска кампании.

<b>Для админов:</b> 
● Выбирайте заказы от рекламодателей прямо в боте.
● Снимайте Reels в ответ на комментарий рекламодателя.
● Получайте оплату за просмотры — чем выше просмотры, тем больше заработок.
<i>Чтобы стать админом, напишите в <a href="https://t.me/boostmedia_support">сюда</a>.</i>

<b>Особенности BoostMedia:</b>
· Живой трафик без раздражающей рекламы — через кликабельные комментарии.
· Аукционная система ставок CPM — чем выше ставка, тем быстрее размещение.
· Минимальный CPM — от $100 за 1 млн показов.

Больше о проекте: <b>@BoostMediaInst</b>
"""

SHARE_TEXTS = [
    """%D0%A7%D0%B5%D0%BA%D0%BD%D0%B8%20%D1%8D%D1%82%D0%BE%D0%B3%D0%BE%20%D0%B1%D0%BE%D1%82%D0%B0,%20%D1%80%D0%B5%D0%B0%D0%BB%D1%8C%D0%BD%D0%BE%20%D0%BF%D0%BE%D0%BC%D0%BE%D0%B3%D0%B0%D0%B5%D1%82%20%D1%80%D0%B0%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D1%82%D1%8C%D1%81%D1%8F%20%D0%B2%20%D1%8D%D0%BC%D0%BE%D1%86%D0%B8%D1%8F%D1%85.%20%D0%9C%D0%BD%D0%B5%20%D0%B7%D0%B0%D1%88%D0%BB%D0%BE,%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82,%20%D0%B8%20%D1%82%D0%B5%D0%B1%D0%B5%20%D0%BF%D1%80%D0%B8%D0%B3%D0%BE%D0%B4%D0%B8%D1%82%D1%81%D1%8F.""", # Чекни этого бота, реально помогает разобраться в эмоциях. Мне зашло, может, и тебе пригодится.
    """%D0%9D%D0%B0%D1%88%D0%B5%D0%BB%20%D0%B3%D0%BE%D0%B4%D0%BD%D0%BE%D0%B3%D0%BE%20%D0%B1%D0%BE%D1%82%D0%B0,%20%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D1%8B%D0%B9%20%D0%BF%D0%BE%D0%BC%D0%BE%D0%B3%D0%B0%D0%B5%D1%82%20%D0%BF%D0%BE%D0%BD%D1%8F%D1%82%D1%8C%20%D1%81%D0%B5%D0%B1%D1%8F.%20%D0%9C%D0%BD%D0%B5%20%D0%BF%D0%BE%D0%BD%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%BE%D1%81%D1%8C,%20%D0%BF%D0%BE%D0%BF%D1%80%D0%BE%D0%B1%D1%83%D0%B9%20%D1%82%D0%BE%D0%B6%D0%B5.""", # Нашел годного бота, который помогает понять себя. Мне понравилось, попробуй тоже.
    """%D0%A1%D0%BB%D1%83%D1%88%D0%B0%D0%B9,%20%D0%BD%D0%B0%D1%82%D0%BA%D0%BD%D1%83%D0%BB%D1%81%D1%8F%20%D0%BD%D0%B0%20%D0%BA%D1%80%D1%83%D1%82%D0%BE%D0%B3%D0%BE%20%D0%B1%D0%BE%D1%82%D0%B0.%20%D0%9E%D0%BD%20%D0%BF%D0%BE%D0%BC%D0%BE%D0%B3%D0%B0%D0%B5%D1%82%20%D1%80%D0%B0%D0%B7%D0%BE%D0%B1%D1%80%D0%B0%D1%82%D1%8C%D1%81%D1%8F%20%D0%B2%20%D1%8D%D0%BC%D0%BE%D1%86%D0%B8%D1%8F%D1%85,%20%D0%BC%D0%BD%D0%B5%20%D0%B7%D0%B0%D1%88%D0%BB%D0%BE.%20%D0%93%D0%BB%D1%8F%D0%BD%D1%8C,%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82,%20%D1%82%D0%BE%D0%B6%D0%B5%20%D0%B7%D0%B0%D0%B9%D0%B4%D0%B5%D1%82.""", # Слушай, наткнулся на крутого бота. Он помогает разобраться в эмоциях, мне зашло. Глянь, может, тоже зайдет.
    """%D0%9F%D1%80%D0%B8%D0%BA%D0%BE%D0%BB%D1%8C%D0%BD%D1%8B%D0%B9%20%D0%B1%D0%BE%D1%82%20%D0%BF%D1%80%D0%BE%20%D1%8D%D0%BC%D0%BE%D1%86%D0%B8%D0%B8%20%D0%B8%20%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D0%B5.%20%D0%9F%D0%BE%D0%BB%D0%B5%D0%B7%D0%BD%D0%B0%D1%8F%20%D1%88%D1%82%D1%83%D0%BA%D0%B0,%20%D1%81%D0%BE%D0%B2%D0%B5%D1%82%D1%83%D1%8E.""" # Прикольный бот про эмоции и состояние. Полезная штука, советую.
]

OFFERS_TEXT = """
<b>Ваши кампании</b>
"""

OFFER_TEXT = """
Оффер #{offer_id}

• Трафик: {offer_actual_views}/{offer_expected_views}кк
• CPM: ${offer_cpm}
• Статус: {offer_status}

Ссылка: {offer_link}
"""

CREATE_OFFER = {
    "link": (
        "<b>Введите ссылку на Reels, который вы хотите продвигать.</b>\n\n"
        "<a href='https://teletype.in/@zelinskiy1/QS4ToBXV3gV#htHq'><i>Про Reels в Instagram, какие ролики лучше, и как их подготовить.</i></a>"
    ),
    "cpm": (
        "<b>Введите желаемый CPM.</b>\n\n"
        "- 🕓 $100 — обычная очередь. Запуск может занять до 24 часов.\n" 
        "- ⚡️ $150 — приоритетная очередь. Запуск в течение 1–4 часов.\n" 
        "- 🚀 $200 — мгновенный запуск. Ваши ролики попадают в ТОП размещения у премиум-админов.\n\n"
        "<a href='https://teletype.in/@zelinskiy1/QS4ToBXV3gV#htHq'><i>Про CPM и как он влияет на продвижение.</i></a>"
    ),
    "views": (
        "<b>Введите кол-во просмотров, которое вы хотите получить.</b>\n\n"
        "<a href='https://teletype.in/@zelinskiy1/QS4ToBXV3gV#htHq'><i>Про кол-во просмотров и как они влияют на продвижение.</i></a>"
    ),
    "done": (
        "<b>Ваша кампания создана и отправлена на модерацию!</b>\n\n"
        "Ожидай пока она будет одобрена.\n"
    ),
    "error": {
        "link": "Неверная ссылка на Reels.",
        "cpm": "Неверный CPM.",
        "views": "Неверное количество просмотров.",
        "balance": {
            "not_enough": "Недостаточно средств на балансе.",
        }
    }
}

ERRORS_TEXT = {
    "link": "Неверная ссылка на Reels.",
    "cpm": "Неверный CPM.",
    "views": "Неверное количество просмотров.",
    "balance": {
        "not_enough": "Недостаточно средств на балансе.",
    },
    "offer": {
        "already_exists": "Оффер с таким ID уже существует.",
        "not_found": "Оффер с таким ID не найден.",
    }
}

OFFER = {
    "group": {
        "moderation": (
            "Оффер #{offer_id}\n\n"
            "• Трафик: {offer_expected_views}\n"
            "• CPM: ${offer_cpm}\n"
            "• Бюджет: {offer_budget}\n"
            "• Reels: {offer_link}\n\n"
            "<b>Информация о клиенте:</b>\n"
            "• ID: #{client_id}\n"
            "• Имя: {client_name} ({client_username})\n"
            "• <b><a href='{client_link}'>Профиль</a></b>\n"
        )
    },
    "dm": {
        "moderation": (
            "🎯 <b>Оффер #{offer_id}</b>\n\n"
            "🔹 <b>CPM:</b> ${offer_cpm}\n"
            "🔹 <b>Бюджет:</b> {offer_budget}\n"
            "🔹 <b>Просмотры:</b> {offer_actual_views}/{offer_expected_views}\n"
            "🔹 <b>Reels:</b> {offer_link}\n\n"
            "<i>{offer_status}</i>\n"
            "<i>Наши модераторы убедятся, что всё выглядит корректно, и скоро он появится в системе для оплаты.</i>"
        ),
        "search_admin": (
            "🎯 <b>Оффер #{offer_id}</b>\n\n"
            "🔹 <b>CPM:</b> ${offer_cpm}\n"
            "🔹 <b>Бюджет:</b> {offer_budget}\n"
            "🔹 <b>Просмотры:</b> {offer_actual_views}/{offer_expected_views}\n"
            "🔹 <b>Reels:</b> {offer_link}\n\n"
            "<i>{offer_status}</i>\n"
            "<i>Идет поиск админов...</i>"
        ),
        "in_progress": (
            "🎯 <b>Оффер #{offer_id}</b>\n\n"
            "🔹 <b>CPM:</b> ${offer_cpm}\n"
            "🔹 <b>Бюджет:</b> {offer_budget}\n"
            "🔹 <b>Просмотры:</b> {offer_actual_views}/{offer_expected_views}\n"
            "🔹 <b>Reels:</b> {offer_link}\n\n"
            "<i>{offer_status}</i>\n"
            "<i>Оффер запущен, ожидайте пока он будет выполнен.</i>"
        ),
        "completed": (
            "🎯 <b>Оффер #{offer_id}</b>\n\n"
            "🔹 <b>CPM:</b> ${offer_cpm}\n"
            "🔹 <b>Бюджет:</b> {offer_budget}\n"
            "🔹 <b>Просмотры:</b> {offer_actual_views}/{offer_expected_views}\n"
            "🔹 <b>Reels:</b> {offer_link}\n\n"
            "<i>{offer_status}</i>\n"
            "<i>Оффер выполнен.</i>"
        ),
        "canceled": (
            "<b>Оффер #{offer_id}</b>\n\n"
            "🔹 <b>CPM:</b> ${offer_cpm}\n"
            "🔹 <b>Бюджет:</b> {offer_budget}\n"
            "🔹 <b>Просмотры:</b> {offer_actual_views}/{offer_expected_views}\n"
            "🔹 <b>Reels:</b> {offer_link}\n\n"
            "<i>{offer_status}</i>\n"
            "<i>Оффер отклонен.</i>"
        ),
        "pending": (
            "🎯 <b>Оффер #{offer_id}</b>\n\n"
            "🔹 <b>CPM:</b> ${offer_cpm}\n"
            "🔹 <b>Бюджет:</b> {offer_budget}\n"
            "🔹 <b>Просмотры:</b> {offer_actual_views}/{offer_expected_views}\n"
            "🔹 <b>Reels:</b> {offer_link}\n\n"
            "<i>{offer_status}</i>\n"
            "<i>Вам нужно оплатить оффер, чтобы он запустился.</i>"
        )
    }
}

PROFILE = {
    "main": (
        "<b>Профиль</b>\n\n"
        "• <b>ID:</b> <code>{user_id}</code>\n"
        "• <b>Баланс USDT:</b> {user_balance}\n"
        "• <b>Дата регистрации:</b> {user_registration_date}\n"
    )
}

BALANCE = {
    "add": (
        "<b>Выберите способ пополнения:</b>"
    ),
    "amount_currency": (
        "<b>Введите предпочитаемую сумму в {currency} для пополнения:</b>\n\n"
        "• Минимальная сумма пополнения: {min_amount}"
    ),
    "error": {
        "amount": "Неверная сумма.",
    },
    "moderation": {
        "add": (
            "<b>Новая заявка на пополнение баланса</b>\n\n"
            "• ID: {user_id} (<a href='{user_link}'>Профиль</a>)\n"
            "• Имя: {user_name} ({user_username})\n"
            "• Сумма: {amount}\n"
            "• Валюта: {currency}\n"
            "• Адрес: <code>{wallet}</code>\n"
            "• Дата: {date}\n"
        )
    }
}


