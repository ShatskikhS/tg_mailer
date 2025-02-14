from aiogram.fsm.state import StatesGroup, State


class NewUserStates(StatesGroup):
    HomeState = State()
    GetInfo = State()
    ConfirmInfo = State()


class UserStates(StatesGroup):
    Feedback = State()


class MailingStates(StatesGroup):
    MailingStart = State()
    PoolOptions = State()
    GetMessageText = State()


class ApplicationsStates(StatesGroup):
    CurrentApplicant = State()


class UserMailingGroupsStates(StatesGroup):
    HomeState = State()
    ChoseUsersState = State()
