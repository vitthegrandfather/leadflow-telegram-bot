from aiogram.fsm.state import State, StatesGroup


class AdminNote(StatesGroup):
    waiting_text = State()
