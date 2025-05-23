from aiogram.fsm.state import State, StatesGroup

class CreateOffer(StatesGroup):
    link = State()
    cpm = State()
    views = State()
    balance = State()