from aiogram.fsm.state import StatesGroup, State


class NewUserStates(StatesGroup):
    HomeState = State()