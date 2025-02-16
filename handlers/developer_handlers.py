from datetime import datetime
import aiofiles.os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from filters.role_filters import RoleFilter
from project_types.enum_types import ChatRole
from project_types.bot_config import BotConfig
from keboards.developer_kb import home_developer_kb, update_roles_kb, USER_MANAGEMENT_KB, HOME_LIST_USERS_KB
from keboards.common_kb import BACK_HOME_TEXT_KB, BACK_HOME_KB, Y_N_KB, HOME_KB
from texts.text_methods import split_message
from texts.common_texts import HOME, ID_IS_TEXT, ID_NOT_IN_LIST, CHOSE_USER_TEXT
from texts.developer_texts import CHOSE_ACTION, users_list_text, CHOSE_NEW_ROLE, ROLE_HAS_UPDATED
from fsms import DeveloperStates
from config_data import DATETIME_FORMAT


router = Router()


@router.message(F.text == 'Домой', RoleFilter(role=ChatRole.DEVELOPER))
async def home(message: Message, state: FSMContext, config: BotConfig):
    await state.clear()
    current_user = config.users[message.from_user.id]
    await message.answer(text=HOME, reply_markup=home_developer_kb(user=current_user))


@router.message(F.text == 'Управление пользователями', RoleFilter(role=ChatRole.DEVELOPER))
@router.message(F.text == 'Назад', DeveloperStates.ChoseUserRoleState)
@router.message(F.text == 'Назад', DeveloperStates.ChoseUserToDeleteState)
async def users_management(message: Message, state: FSMContext):
    await message.answer(text=CHOSE_ACTION, reply_markup=USER_MANAGEMENT_KB)
    await state.set_state(DeveloperStates.UserManagement)


# ====================== Change ChatRole handlers ======================

@router.message(F.text == 'Изменить роль пользователя', DeveloperStates.UserManagement)
@router.message(F.text == 'Назад', DeveloperStates.ChoseNewRolesState)
@router.message(F.text == 'К списку пользователей', RoleFilter(role=ChatRole.DEVELOPER))
async def change_role_users(message: Message, state: FSMContext, config: BotConfig):
    users_list = [user for user in config.users.values() if user.role != ChatRole.APPLICANT]
    user_texts = split_message(text=users_list_text(users=users_list))
    for user_text in user_texts:
        await message.answer(text=user_text)
    await message.answer(text='Для продолжения отправьте ID пользователя боту как обычное сообщение',
                         reply_markup=BACK_HOME_TEXT_KB)
    await state.update_data(users=users_list)
    await state.set_state(DeveloperStates.ChoseUserRoleState)


@router.message(DeveloperStates.ChoseUserRoleState)
async def show_user_data(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    users_list = data['users']
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(text=ID_IS_TEXT)
        user_texts = split_message(text=users_list_text(users=users_list))
        for user_text in user_texts:
            await message.answer(text=user_text)
        await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)
        return
    if user_id not in [user.id for user in users_list]:
        await message.answer(text=ID_NOT_IN_LIST)
        user_texts = split_message(text=users_list_text(users=users_list))
        for user_text in user_texts:
            await message.answer(text=user_text)
        await message.answer(text=CHOSE_USER_TEXT, reply_markup=BACK_HOME_TEXT_KB)
        return
    current_user = config.users[user_id]

    await state.update_data(user_id=user_id)
    await message.answer(text=current_user.represent_user_full())
    await message.answer(text=CHOSE_NEW_ROLE, reply_markup=update_roles_kb(user=current_user))
    await state.set_state(DeveloperStates.ChoseNewRolesState)


@router.message(DeveloperStates.ChoseNewRolesState)
async def change_role(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    user_id = data['user_id']
    await config.alter_user_role(user_id=user_id, new_role=ChatRole(message.text))
    await message.answer(text=config.users[user_id].represent_user_full())
    await message.answer(text=ROLE_HAS_UPDATED, reply_markup=HOME_LIST_USERS_KB)
    await state.clear()


# ====================== Delete user ======================

@router.message(F.text == 'Удалить пользователя', DeveloperStates.UserManagement)
@router.message(F.text == 'Нет', DeveloperStates.DeleteUserState)
async def chose_user_to_remove(message: Message, state: FSMContext, config: BotConfig):
    users_list = list(config.users.values())
    user_texts = split_message(text=users_list_text(users=users_list))
    for user_text in user_texts:
        await message.answer(text=user_text)
    await message.answer(text='Для удаления пользователя отправьте его ID боту как обычное сообщение',
                         reply_markup=BACK_HOME_TEXT_KB)
    await state.set_state(DeveloperStates.ChoseUserToDeleteState)


@router.message(DeveloperStates.ChoseUserToDeleteState)
async def show_user_to_delete(message: Message, state: FSMContext, config: BotConfig):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(text=ID_IS_TEXT, reply_markup=BACK_HOME_KB)
        return

    await message.answer(text=config.users[user_id].represent_user_full())
    await message.answer(text='Подтверждаете удаление?', reply_markup=Y_N_KB)
    await state.update_data(user_id=user_id)
    await state.set_state(DeveloperStates.DeleteUserState)


@router.message(F.text == 'Да', DeveloperStates.DeleteUserState)
async def delete_user(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    user_id = data['user_id']
    for group in config.users[user_id].groups:
        await config.drop_user_mailing_group(user_id=user_id, group=group)
    await config.get_user_info(user_id=user_id)
    await config.remove_user_by_id(user_id=user_id)
    await state.clear()
    await message.answer(text='Пользователь успешно удален.', reply_markup=HOME_KB)


# ====================== Generate xlsx ======================

@router.message(F.text == 'Скачать xlsx таблицу', DeveloperStates.UserManagement)
async def generate_xlsx(message: Message, config: BotConfig):
    path = f'data/all_users{datetime.now().strftime(DATETIME_FORMAT)}.xlsx'
    await config.async_save_to_excel(path=path)

    inp_f = FSInputFile(path=path)
    await message.answer_document(document=inp_f)

    await aiofiles.os.remove(path)
