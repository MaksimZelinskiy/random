from aiogram import Router
from .create import router as create_router
from .view import router as view_router

router = Router()
router.include_routers(create_router, view_router)

__all__ = ["router"] 