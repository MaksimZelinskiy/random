from .admins import router as admins_router
from .client import router as main_router
from .system import router as system_router

from aiogram import Router

router = Router()   
router.include_router(main_router)
router.include_router(admins_router)
router.include_router(system_router)
    
__all__ = ['router']
