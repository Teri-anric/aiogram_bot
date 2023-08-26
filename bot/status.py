from aiogram.fsm.state import StatesGroup, State


class InputPostStates(StatesGroup):
    in_text = State()
    in_photo = State()
