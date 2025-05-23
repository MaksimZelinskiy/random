from typing import Optional
 
from pydantic import BaseModel, Field


class TelegramUser(BaseModel):
    id: int = Field(description="Unique identifier for the user or bot")
    is_bot: Optional[bool] = Field(
        default=None,
        description="True if this user is a bot. Returns in the receiver field only",
    )
    first_name: str = Field(description="First name of the user or bot")
    last_name: Optional[str] = Field(
        default=None, description="Last name of the user or bot"
    )
    username: Optional[str] = Field(
        default=None, description="Username of the user or bot"
    )
    language_code: Optional[str] = Field(
        default=None, description="IETF language tag of the user's language"
    )
    is_premium: Optional[bool] = Field(
        default=None,
        description="True if this user is a Telegram Premium user",
    )
    added_to_attachment_menu: Optional[bool] = Field(
        default=None,
        description="True if this user added the bot to the attachment menu",
    )
    start_param: Optional[str] = Field(
        default=None,
        description="Startapp code",
    )
    allows_write_to_pm: Optional[bool] = Field(
        default=None,
        description="True if this user allowed the bot to message them",
    )
    photo_url: Optional[str] = Field(
        default=None,
        description="URL of the user's profile photo (JPEG or SVG format)",
    )

    class Config:
        from_attributes = True