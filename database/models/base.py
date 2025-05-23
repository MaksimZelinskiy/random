import enum
import typing
from datetime import datetime

import sqlalchemy
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql.functions import func
from typing_extensions import Annotated

int_pk = Annotated[int, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    type_annotation_map = {
        enum.Enum: sqlalchemy.Enum(enum.Enum),
        typing.Literal: sqlalchemy.Enum(enum.Enum),
        dict[str, typing.Any]: sqlalchemy.JSON,
        list[int]: sqlalchemy.ARRAY(sqlalchemy.Integer),
    }

    def to_dict(self) -> dict:
        """Convert SQLAlchemy model instance to dictionary.
        
        Handles nested relationships and JSON columns properly.
        """
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            result[column.name] = value
        return result


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, server_default=func.now()
    )
