from aiogram.fsm.state import StatesGroup, State


class GetDataState(StatesGroup):
    answer_input = State()
    text_input = State()
    confirmation_input = State()


