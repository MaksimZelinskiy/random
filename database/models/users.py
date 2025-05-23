from ctypes.wintypes import HKEY
from datetime import datetime
from typing import Literal

from sqlalchemy import BIGINT, func, JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base

STATUS = Literal["active", "block"]

class User(Base):
    __tablename__ = "users"
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True)

    name: Mapped[str] = mapped_column()
    username: Mapped[str | None] = mapped_column(default=None)

    is_active: Mapped[bool] = mapped_column(default=True)    

    lang: Mapped[str | None] = mapped_column(default=None)
    referrer_id: Mapped[str | None] = mapped_column(default="search")
    
    date_reg: Mapped[datetime] = mapped_column(default=func.now())
    

class UserLogin(Base):
    __tablename__ = "user_login"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(BIGINT)
    data: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(default=func.now())


class UserMailings(Base):
    __tablename__ = "user_mailings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created_by_admin_id: Mapped[int] = mapped_column(BIGINT) # Кто инициировал рассылку (создатель розыгрыша / админ)
    
    # mailing_id: Mapped[int | None] = mapped_column(Integer) # ID рассылки 

    task_type: Mapped[str] = mapped_column(String) #  ('mailing', 'publication', 'results') # Тип задачи (рассылка, публикация розыгрыша, публикация итогов)
    target_id: Mapped[str] = mapped_column(String) # Куда отправлять
    msg_id: Mapped[int | None] = mapped_column(Integer) # ID сообщения (если отправлено)

    message_type: Mapped[str] = mapped_column(String) #  ('text', 'photo') # Тип сообщения
    media_file_id: Mapped[str | None] = mapped_column(String) # ID медиафайла (если есть)
    text: Mapped[str | None] = mapped_column(String) # Текст сообщения / caption

    reply_markup: Mapped[dict] = mapped_column(JSON) # Клавиатура

    scheduled_at: Mapped[datetime] = mapped_column(default=func.now()) # Время запланированной отправки
    sent_at: Mapped[datetime | None] = mapped_column(default=None) # Время фактической отправки

    status: Mapped[str] = mapped_column(default="pending") # Статус обработки

    retry_count: Mapped[int] = mapped_column(default=0) # Число попыток

    error_message: Mapped[str | None] = mapped_column(String) # Ошибка (если не отправлено)

    created_at: Mapped[datetime] = mapped_column(default=func.now()) # Время создания


