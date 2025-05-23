from datetime import datetime
import json
from fastapi import APIRouter, Depends, HTTPException, Query, Body
from enum import Enum
from typing import Optional, List, Literal

from models.telegram import TelegramUser
from clients.users import UsersClient
from database import RequestsRepo
from dependencies import get_repo, get_user_from_webdata
from schemas.main import SuccessResponse, ErrorResponse
from tg_bot.utils import send_hello_message_to_user
from fastapi import BackgroundTasks
from fastapi import Request


users_router = APIRouter(
    tags=["users"]
)


@users_router.post("/users/login/{startup_code}", response_model=SuccessResponse)
async def user_login(
    request: Request,
    startup_code: str,
    repo: RequestsRepo = Depends(get_repo),
    user: TelegramUser = Depends(get_user_from_webdata)
) -> SuccessResponse:
    """
    Login user to startup
    """
    users_client = UsersClient(repo, user)
    
    if not await users_client.get_user_if_exists(user.id):
        await users_client.register_user(user, startup_code)
        await send_hello_message_to_user(user.id)
            
    await users_client.track_user_login(
        user_id=user.id,
        user_ip=request.state.real_ip,
        startapp_code=startup_code
    )
        
    return SuccessResponse(
        message="User retrieved successfully",
        data={"user": user}
    )
    
    