from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from database.models.base import Base


# Таблица для связи пользователей с администраторами
class UserAdminBind(Base):
    __tablename__ = "user_admin_bind"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    admin_id: Mapped[int] = mapped_column(Integer)
    giveaway_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default=func.now())


# Таблица для связи каналы админов
class AdminChannelBind(Base):
    __tablename__ = "admin_channel_bind"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    admin_id: Mapped[int] = mapped_column(Integer)
    channel_id: Mapped[str] = mapped_column(String)
    
    channel_title: Mapped[str] = mapped_column(String)
    
    channels_username: Mapped[str] = mapped_column(String)  
    channels_link: Mapped[str] = mapped_column(String)  
    
    channel_status: Mapped[str] = mapped_column(String) # status of channel (active, blocked)
    
    created_at: Mapped[datetime] = mapped_column(default=func.now())


# таблица для хранение подписок на розыгрыши
class UserSubscription(Base):
    __tablename__ = "user_subscription"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer)
    giveaway_id: Mapped[str] = mapped_column(String)
    channel_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    
