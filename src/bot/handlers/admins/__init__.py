from .mailing import router as mailing_router
from .main import router as main_router
from .stats import router as stats_router

from aiogram import Router
router = Router()

router.include_router(mailing_router)
router.include_router(main_router)
router.include_router(stats_router)

__all__ = [
    router
]