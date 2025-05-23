from .add import router as add_router

from aiogram import Router

router = Router()
router.include_routers(add_router)

__all__ = ["router"] 