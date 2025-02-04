from aiogram.fsm.state import StatesGroup, State


class NewUserStates(StatesGroup):
    HomeState = State()


class UserStates(StatesGroup):
    Feedback = State()