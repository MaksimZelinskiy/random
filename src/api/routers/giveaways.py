

# get giveaway
# join to giveaway


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


@users_router.post("/users/join/{giveaway_id}", response_model=SuccessResponse)
async def user_join_giveaway(
    request: Request,
    giveaway_id: str,
    repo: RequestsRepo = Depends(get_repo),
    user: TelegramUser = Depends(get_user_from_webdata)
) -> SuccessResponse:
    """
    Join user to giveaway
    """
    
    # check if giveaway exists
    giveaway = await repo.giveaways.get_giveaway(giveaway_id)
    if not giveaway:
        raise HTTPException(status_code=404, detail="Giveaway not found")
    
    # get users who joined to giveaway
    users_giveaway = await repo.giveaways.get_users_giveaway(giveaway_id)
    
    # check if user is already joined to giveaway
    if user.id in users_giveaway:
        raise HTTPException(status_code=400, detail="User already joined to giveaway")
    
    # сделать провкрку на ТВИНК аккаунты
    
    # add user to giveaway
    await repo.giveaways.join_user_to_giveaway(giveaway_id, user.id)
        
    return SuccessResponse(
        message="User joined to giveaway successfully",
        data={"giveaway": giveaway}
    )
    
@users_router.get("/giveaways/{giveaway_id}", response_model=SuccessResponse)   
async def get_giveaway(
    giveaway_id: str,
    repo: RequestsRepo = Depends(get_repo)
) -> SuccessResponse:
    """
        Get giveaway
    """
    
    giveaway = await repo.giveaways.get_giveaway(giveaway_id)
    if not giveaway:
        raise HTTPException(status_code=404, detail="Giveaway not found")
    
    return SuccessResponse(
        message="Giveaway retrieved successfully",  
        data={"giveaway": giveaway}
    )
    
    
    
    