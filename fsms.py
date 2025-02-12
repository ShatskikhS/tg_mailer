from aiogram.fsm.state import StatesGroup, State


class NewUserStates(StatesGroup):
    HomeState = State()


class UserStates(StatesGroup):
    Feedback = State()


class MailingStates(StatesGroup):
    MailingStart = State()
    PoolOptions = State()
    GetMessageText = State()