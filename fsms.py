from aiogram.fsm.state import StatesGroup, State


class NewUserStates(StatesGroup):
    home_state = State()
    get_info = State()
    confirm_info = State()
    add_to_group = State()
    chose_group = State()


class UserStates(StatesGroup):
    feedback = State()


class MailingStates(StatesGroup):
    mailing_start = State()
    pool_options = State()
    get_message_text = State()
    group_buttons = State()
    recipients = State()


class ApplicationsStates(StatesGroup):
    CurrentApplicant = State()


class UserMailingGroupsStates(StatesGroup):
    home_state = State()
    chose_users_state = State()
    chose_group_state = State()
    chose_not_group_state = State()
    chose_out_of_group_state = State()
    update_group_state = State()


class DeveloperStates(StatesGroup):
    user_management = State()
    chose_user_role_state = State()
    chose_new_roles_state = State()
    chose_user_to_delete_state = State()
    delete_user_state = State()
    mailing_management_state = State()
    get_group_name_state = State()
    get_group_description_state = State()
    add_group_state = State()
    chose_group_to_delete_state = State()
    confirm_group_to_delete_state = State()
