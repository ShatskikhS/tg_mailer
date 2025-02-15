from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.role_filters import RoleFilter
from project_types.bot_config import BotConfig
from project_types.user_type import UserType
from project_types.enum_types import ChatRole, MailingGroup
from fsms import UserMailingGroupsStates
from texts.common_texts import USER_GROUPS_HOME_TEXT, CHOSE_USER_TEXT, ID_IS_TEXT, ID_NOT_IN_LIST
from texts.text_methods import get_users_groups_text
from keboards.common_kb import USER_GROUPS_HOME_KB, BACK_HOME_TEXT_KB, HOME_KB, groups_home_kb, edit_groups_kb


router = Router()


@router.message(F.text == 'Управление пользовательскими группами', RoleFilter([ChatRole.ADMIN, ChatRole.DEVELOPER]))
@router.message(F.text == 'Назад', UserMailingGroupsStates.ChoseGroupState)
@router.message(F.text == 'Назад', UserMailingGroupsStates.ChoseNotGroupState)
@router.message(F.text == 'Назад', UserMailingGroupsStates.ChoseUsersState)
async def user_groups_home(message: Message, state: FSMContext):
    await message.answer(text=USER_GROUPS_HOME_TEXT, reply_markup=USER_GROUPS_HOME_KB)
    await state.set_state(UserMailingGroupsStates.HomeState)


@router.message(F.text == 'Все пользователи', UserMailingGroupsStates.HomeState)
@router.message(F.text == 'Пользователи без группы', UserMailingGroupsStates.HomeState)
async def all_users(message: Message, state: FSMContext, config: BotConfig):
    if message.text == 'Все пользователи':
        users_list = [user for user in config.users.values() if user.role != ChatRole.APPLICANT]
    else:
        users_list = [user for user in config.users.values() if user.role != ChatRole.APPLICANT and user.groups == []]
    await message.answer(text=get_users_groups_text(users_list))
    await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)

    await state.update_data(users=users_list)
    await state.set_state(UserMailingGroupsStates.ChoseUsersState)

@router.message(F.text == 'Пользователи группы', UserMailingGroupsStates.HomeState)
@router.message(F.text == 'Пользователи не в группе', UserMailingGroupsStates.HomeState)
@router.message(F.text == 'Назад', UserMailingGroupsStates.ChoseUsersState)
async def chose_group(message: Message, state: FSMContext):
    line1_names = [group.value for group in MailingGroup]
    await message.answer(text='Выберите группу', reply_markup=groups_home_kb(line1_names))
    if message.text == 'Пользователи группы':
        await state.set_state(UserMailingGroupsStates.ChoseGroupState)
    else:
        await state.set_state(UserMailingGroupsStates.ChoseNotGroupState)


@router.message(UserMailingGroupsStates.ChoseGroupState)
@router.message(UserMailingGroupsStates.ChoseNotGroupState)
@router.message(F.text == 'Назад', UserMailingGroupsStates.ChoseUsersState)
@router.message(F.text == 'Назад', UserMailingGroupsStates.UpdateGroupState)
async def group_users(message: Message, state: FSMContext, config: BotConfig):
    current_state = await state.get_state()
    if current_state == UserMailingGroupsStates.ChoseGroupState:
        users_list = [user for user in config.users.values() if MailingGroup(message.text) in user.groups]
    else:
        users_list = [user for user in config.users.values() if MailingGroup(message.text) not in user.groups and user.role != ChatRole.APPLICANT]
    await message.answer(text=get_users_groups_text(users_list))
    await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)

    await state.update_data(users=users_list)
    await state.set_state(UserMailingGroupsStates.ChoseUsersState)


@router.message(UserMailingGroupsStates.ChoseUsersState)
async def show_user_data(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    users_list: List[UserType] = data.get('users')
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(text=ID_IS_TEXT)
        await message.answer(text=get_users_groups_text(users_list))
        await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)
        return
    if user_id not in [user.id for user in users_list]:
        await message.answer(text=ID_NOT_IN_LIST)
        await message.answer(text=get_users_groups_text(users_list))
        await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)
        return

    current_user = config.users[user_id]

    await message.answer(text=current_user.represent_user_with_groups())
    await message.answer(text='Выберете действие', reply_markup=edit_groups_kb(current_user))
    await state.update_data(user_id=user_id)
    await state.set_state(UserMailingGroupsStates.UpdateGroupState)


@router.message(UserMailingGroupsStates.UpdateGroupState)
async def update_user_data(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    user_id = data['user_id']
    new_group = MailingGroup(message.text.split()[-1])
    if message.text.startswith('Добавить'):
        await config.add_user_to_mailing_group(user_id, new_group)
        await message.answer(text=f'Пользователь успешно добавлен в {new_group.value}', reply_markup=HOME_KB)
    else:
        await config.drop_user_mailing_group(user_id, new_group)
        await message.answer(text=f'Пользователь успешно удален из {new_group.value}', reply_markup=HOME_KB)
    await state.clear()
