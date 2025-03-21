from typing import List

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.role_filters import RoleFilter
from project_types.bot_config import BotConfig
from project_types.user_type import UserType
from project_types.enum_types import ChatRole
from fsms import UserMailingGroupsStates, DeveloperStates
from texts.common_texts import USER_GROUPS_HOME_TEXT, CHOSE_USER_TEXT, ID_IS_TEXT, ID_NOT_IN_LIST
from texts.text_methods import get_users_groups_text
from keboards.common_kb import USER_GROUPS_HOME_KB, BACK_HOME_TEXT_KB, HOME_KB, groups_builder_kb, edit_groups_builder_kb


router = Router()


@router.message(F.text == 'Управление пользовательскими группами', RoleFilter(ChatRole.ADMIN))
@router.message(F.text == 'Изменить группу', DeveloperStates.user_management)
@router.message(F.text == 'Назад', UserMailingGroupsStates.chose_group_state)
@router.message(F.text == 'Назад', UserMailingGroupsStates.chose_not_group_state)
@router.message(F.text == 'Назад', UserMailingGroupsStates.chose_users_state)
async def user_groups_home(message: Message, state: FSMContext):
    await message.answer(text=USER_GROUPS_HOME_TEXT, reply_markup=USER_GROUPS_HOME_KB)
    await state.set_state(UserMailingGroupsStates.home_state)


@router.message(F.text == 'Все пользователи', UserMailingGroupsStates.home_state)
@router.message(F.text == 'Пользователи без группы', UserMailingGroupsStates.home_state)
async def all_users(message: Message, state: FSMContext, config: BotConfig):
    if message.text == 'Все пользователи':
        users_list = [user for user in config.users.values() if user.role != ChatRole.APPLICANT]
    else:
        users_list = [user for user in config.users.values() if user.role != ChatRole.APPLICANT and user.groups == []]
    if not users_list:
        await message.answer(text='Нет пользователей с заданными параметрами')
        return
    await message.answer(text=get_users_groups_text(users_list))
    await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)

    await state.update_data(users=users_list)
    await state.set_state(UserMailingGroupsStates.chose_users_state)

@router.message(F.text == 'Пользователи группы', UserMailingGroupsStates.home_state)
@router.message(F.text == 'Пользователи не в группе', UserMailingGroupsStates.home_state)
@router.message(F.text == 'Назад', UserMailingGroupsStates.chose_users_state)
async def chose_group(message: Message, state: FSMContext, config: BotConfig):
    line1_names = list(config.all_groups.keys())
    await message.answer(text='Выберите группу', reply_markup=groups_builder_kb(line1_names))
    if message.text == 'Пользователи группы':
        await state.set_state(UserMailingGroupsStates.chose_group_state)
    else:
        await state.set_state(UserMailingGroupsStates.chose_not_group_state)


@router.message(UserMailingGroupsStates.chose_group_state)
@router.message(UserMailingGroupsStates.chose_not_group_state)
@router.message(F.text == 'Назад', UserMailingGroupsStates.chose_users_state)
@router.message(F.text == 'Назад', UserMailingGroupsStates.update_group_state)
async def group_users(message: Message, state: FSMContext, config: BotConfig):
    current_state = await state.get_state()
    if current_state == UserMailingGroupsStates.chose_group_state:
        users_list = [user for user in config.users.values() if message.text in user.groups]
    else:
        users_list = [user for user in config.users.values() if message.text not in user.groups and user.role != ChatRole.APPLICANT]
    if not users_list:
        await message.answer('Нет пользователей с заданными параметрами')
        return
    await message.answer(text=get_users_groups_text(users_list))
    await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)

    await state.update_data(users=users_list)
    await state.set_state(UserMailingGroupsStates.chose_users_state)


@router.message(UserMailingGroupsStates.chose_users_state)
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

    await message.answer(text=current_user.represent_user_full())

    await message.answer(text='Выберете действие',
                         reply_markup=edit_groups_builder_kb(user=current_user, all_groups=list(config.all_groups.keys())))
    await state.update_data(user_id=user_id)
    await state.set_state(UserMailingGroupsStates.update_group_state)


@router.message(UserMailingGroupsStates.update_group_state)
async def update_user_data(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    user_id = data['user_id']
    new_group = message.text.replace('Добавить в ', '').replace('Удалить из ', '')
    if message.text.startswith('Добавить'):
        await config.add_user_to_mailing_group(user_id, new_group)
        await message.answer(text=f'Пользователь успешно добавлен в {new_group}', reply_markup=HOME_KB)
    else:
        await config.remove_user_form_mailing_group(user_id, new_group)
        await message.answer(text=f'Пользователь успешно удален из {new_group}', reply_markup=HOME_KB)
    await state.clear()
