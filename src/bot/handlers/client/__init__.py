from .start import router as start_router   
from .channels import router as channels_router
from .giveaways import router as giveaways_router

from aiogram import Router  

router = Router()
router.include_router(start_router)
router.include_router(channels_router)
router.include_router(giveaways_router)

__all__ = ['router']
