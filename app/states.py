from aiogram.fsm.state import StatesGroup, State


class Register(StatesGroup):
    name = State()
    number = State()