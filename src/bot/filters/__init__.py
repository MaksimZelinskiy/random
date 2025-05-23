from aiogram import Dispatcher

from .check_reg import IsPrivate

def setup1(dp: Dispatcher):
    dp.filters_factory.bind(IsPrivate)
    

