from datetime import datetime
from typing import Literal

from sqlalchemy import BIGINT, func, JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base

STATUS = Literal["active", "block"]


# Таблица для розыгрышей
class Giveaway(Base):
    __tablename__ = "giveaways"
    
    id: Mapped[str] = mapped_column(String, primary_key=True) # uuid
    admin_id: Mapped[int] = mapped_column(Integer) 
    
    publish_channels: Mapped[dict] = mapped_column(JSON) # каналы, в которых будет проходить розыгрыш,
    required_channels: Mapped[dict] = mapped_column(JSON) # каналы, в которых нужно подписаться, для участия в розыгрыше
    
    view_details: Mapped[dict] = mapped_column(JSON) # детали сообщения розгрыша 
    
    count_participants: Mapped[int] = mapped_column(default=0) # количество участников в данный момент
    count_winners: Mapped[int] = mapped_column(default=0) # количество победителей, которые будут выбраны
    
    use_boost: Mapped[bool] = mapped_column(default=False) # использовать ли boost для розыгрыша    
    use_capha: Mapped[bool] = mapped_column(default=False) # использовать ли capha для розыгрыша    
    use_block_twinks: Mapped[bool] = mapped_column(default=False) # использовать ли блокировку твинков для розыгрыша    
    
    start_at: Mapped[datetime] = mapped_column()
    ends_at: Mapped[datetime] = mapped_column()
    
    is_published: Mapped[bool] = mapped_column(default=False)    
    status: Mapped[STATUS] = mapped_column(default="active") # статус розыгрыша (wait_start, active, winners_selection, finished)
    
    created_at: Mapped[datetime] = mapped_column(default=func.now())




# Таблица для участников розыгрыша
class GiveawayParticipant(Base):
    __tablename__ = "giveaway_participants"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    giveaway_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    user_ip: Mapped[str] = mapped_column(String)
        
    count_boost: Mapped[int] = mapped_column(default=0)
    
    status: Mapped[str] = mapped_column(String) # статус участника (active, blocked)
    
    joined_at: Mapped[datetime] = mapped_column(default=func.now()) 

    
    

# Таблица для победителей
class GiveawayWinner(Base):
    __tablename__ = "giveaway_winners"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    giveaway_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer)
    
    place: Mapped[int] = mapped_column(Integer) 
    type: Mapped[str] = mapped_column(String) # type of winner (main, additional)
    
    selected_at: Mapped[datetime] = mapped_column(default=func.now())



"""
CREATE TABLE giveaways (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id INT NOT NULL,
    publish_channels JSONB NOT NULL,
    required_channels JSONB NOT NULL,
    view_details JSONB NOT NULL,    
    count_participants INT NOT NULL DEFAULT 0,
    count_winners INT NOT NULL DEFAULT 0,
    use_boost BOOLEAN NOT NULL DEFAULT FALSE,
    use_capha BOOLEAN NOT NULL DEFAULT FALSE,
    use_block_twinks BOOLEAN NOT NULL DEFAULT FALSE,
    start_at TIMESTAMP NOT NULL,
    ends_at TIMESTAMP NOT NULL, 
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(255) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);  

CREATE TABLE giveaway_participants (        
    id SERIAL PRIMARY KEY,
    giveaway_id INT NOT NULL,
    user_id INT NOT NULL,
    user_ip VARCHAR(255) NOT NULL,
    count_boost INT NOT NULL DEFAULT 0,
    status VARCHAR(255) NOT NULL,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE giveaway_winners (
    id SERIAL PRIMARY KEY,
    giveaway_id INT NOT NULL,
    user_id INT NOT NULL,
    place INT NOT NULL,
    type VARCHAR(255) NOT NULL,
    selected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);              
"""



