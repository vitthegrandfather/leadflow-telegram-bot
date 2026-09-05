from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    full_name = State()
    phone = State()
    category = State()
    description = State()
    contact_method = State()
    confirm = State()
