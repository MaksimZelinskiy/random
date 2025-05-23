from .main import router as main_router
from .add import router as add_router

from aiogram import Router

router = Router()
router.include_routers(
    main_router, 
    add_router
)

__all__ = ["router"]     
