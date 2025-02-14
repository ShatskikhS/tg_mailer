from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.role_filters import RoleFilter
from project_types.bot_config import BotConfig
from project_types.enum_types import ChatRole, MailingGroup
from fsms import UserMailingGroupsStates
from texts.common_texts import USER_GROUPS_HOME_TEXT, CHOSE_USER_TEXT
from texts.text_methods import get_users_groups_text
from keboards.common_kb import USER_GROUPS_HOME_KB, BACK_HOME_TEXT_KB


router = Router()


@router.message(F.text == 'Управление пользовательскими группами', RoleFilter([ChatRole.ADMIN, ChatRole.DEVELOPER]))
async def user_groups_home(message: Message, state: FSMContext):
    await message.answer(text=USER_GROUPS_HOME_TEXT, reply_markup=USER_GROUPS_HOME_KB)
    await state.set_state(UserMailingGroupsStates.HomeState)


@router.message(F.text == 'Все пользователи', UserMailingGroupsStates.HomeState)
async def all_users(message: Message, state: FSMContext, config: BotConfig):
    users_list = [user for user in config.users.values() if user.groups]
    await message.answer(text=get_users_groups_text(users_list))
    await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)

    await state.set_state(UserMailingGroupsStates.ChoseUsersState)

@router.message(F.text == 'Пользователи по группам', UserMailingGroupsStates.ChoseUsersState)
async def chose_group(message: Message, state: FSMContext):
    pass

