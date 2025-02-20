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
    ChoseGroupState = State()
    ChoseNotGroupState = State()
    ChoseOutOfGroupState = State()
    UpdateGroupState = State()


class DeveloperStates(StatesGroup):
    UserManagement = State()
    ChoseUserRoleState = State()
    ChoseNewRolesState = State()
    ChoseUserToDeleteState = State()
    DeleteUserState = State()
    MailingManagementState = State()
    GetGroupNameState = State()
    GetGroupDescriptionState = State()
    AddGroupState = State()
    ChoseGroupToDeleteState = State()
    ConfirmGroupToDeleteState = State()
