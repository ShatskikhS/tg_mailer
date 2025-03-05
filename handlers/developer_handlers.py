from datetime import datetime
import aiofiles.os

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from filters.role_filters import RoleFilter
from project_types.enum_types import ChatRole
from project_types.bot_config import BotConfig
from keboards.developer_kb import home_developer_kb, update_roles_kb, USER_MANAGEMENT_KB, HOME_LIST_USERS_KB, MAILING_MANAGEMENT_KB, groups_to_delete_kb
from keboards.common_kb import BACK_HOME_TEXT_KB, BACK_HOME_KB, Y_N_KB, HOME_KB, CONTINUE_BACK_HOME_KB
from texts.text_methods import split_message
from texts.common_texts import HOME, ID_IS_TEXT, ID_NOT_IN_LIST, CHOSE_USER_TEXT
from texts.developer_texts import CHOSE_ACTION, users_list_text, CHOSE_NEW_ROLE, ROLE_HAS_UPDATED, mailing_management_text, INPUT_GROUP_NAME, input_group_description_text, confirm_new_group_data, confirm_group_delete_text
from fsms import DeveloperStates
from config_data import DATETIME_FORMAT


router = Router()


@router.message(F.text == 'Домой', RoleFilter(role=ChatRole.DEVELOPER))
async def home(message: Message, state: FSMContext, config: BotConfig):
    await state.clear()
    current_user = config.users[message.from_user.id]
    await message.answer(text=HOME, reply_markup=home_developer_kb(user=current_user))


@router.message(F.text == 'Управление пользователями', RoleFilter(role=ChatRole.DEVELOPER))
@router.message(F.text == 'Назад', DeveloperStates.chose_user_role_state)
@router.message(F.text == 'Назад', DeveloperStates.chose_user_to_delete_state)
async def users_management(message: Message, state: FSMContext):
    await message.answer(text=CHOSE_ACTION, reply_markup=USER_MANAGEMENT_KB)
    await state.set_state(DeveloperStates.user_management)


# ====================== Change ChatRole handlers ======================

@router.message(F.text == 'Изменить роль пользователя', DeveloperStates.user_management)
@router.message(F.text == 'Назад', DeveloperStates.chose_new_roles_state)
@router.message(F.text == 'К списку пользователей', RoleFilter(role=ChatRole.DEVELOPER))
async def change_role_users(message: Message, state: FSMContext, config: BotConfig):
    users_list = [user for user in config.users.values() if user.role != ChatRole.APPLICANT]
    user_texts = split_message(text=users_list_text(users=users_list))
    for user_text in user_texts:
        await message.answer(text=user_text)
    await message.answer(text='Для продолжения отправьте ID пользователя боту как обычное сообщение',
                         reply_markup=BACK_HOME_TEXT_KB)
    await state.update_data(users=users_list)
    await state.set_state(DeveloperStates.chose_user_role_state)


@router.message(DeveloperStates.chose_user_role_state)
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
    await state.set_state(DeveloperStates.chose_new_roles_state)


@router.message(DeveloperStates.chose_new_roles_state)
async def change_role(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    user_id = data['user_id']
    await config.alter_user_role(user_id=user_id, new_role=ChatRole(message.text))
    await message.answer(text=config.users[user_id].represent_user_full())
    await message.answer(text=ROLE_HAS_UPDATED, reply_markup=HOME_LIST_USERS_KB)
    await state.clear()


# ====================== Delete user ======================

@router.message(F.text == 'Удалить пользователя', DeveloperStates.user_management)
@router.message(F.text == 'Нет', DeveloperStates.delete_user_state)
async def chose_user_to_remove(message: Message, state: FSMContext, config: BotConfig):
    users_list = list(config.users.values())
    user_texts = split_message(text=users_list_text(users=users_list))
    for user_text in user_texts:
        await message.answer(text=user_text)
    await message.answer(text='Для удаления пользователя отправьте его ID боту как обычное сообщение',
                         reply_markup=BACK_HOME_TEXT_KB)
    await state.set_state(DeveloperStates.chose_user_to_delete_state)


@router.message(DeveloperStates.chose_user_to_delete_state)
async def show_user_to_delete(message: Message, state: FSMContext, config: BotConfig):
    try:
        user_id = int(message.text.strip())
    except ValueError:
        await message.answer(text=ID_IS_TEXT, reply_markup=BACK_HOME_KB)
        return

    await message.answer(text=config.users[user_id].represent_user_full())
    await message.answer(text='Подтверждаете удаление?', reply_markup=Y_N_KB)
    await state.update_data(user_id=user_id)
    await state.set_state(DeveloperStates.delete_user_state)


@router.message(F.text == 'Да', DeveloperStates.delete_user_state)
async def delete_user(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    user_id = data['user_id']
    for group in config.users[user_id].groups:
        await config.remove_user_form_mailing_group(user_id=user_id, group=group)
    await config.get_user_info(user_id=user_id)
    await config.remove_user_by_id(user_id=user_id)
    await state.clear()
    await message.answer(text='Пользователь успешно удален.', reply_markup=HOME_KB)


# ====================== Generate xlsx ======================

@router.message(F.text == 'Скачать xlsx таблицу', DeveloperStates.user_management)
async def generate_xlsx(message: Message, config: BotConfig):
    path = f'data/all_users{datetime.now().strftime(DATETIME_FORMAT)}.xlsx'
    await config.async_save_to_excel(path=path)

    inp_f = FSInputFile(path=path)
    await message.answer_document(document=inp_f)

    await aiofiles.os.remove(path)


# ====================== Mailing management ======================

@router.message(F.text == 'Управление группами рассылок', RoleFilter(ChatRole.DEVELOPER))
@router.message(F.text == 'Назад', DeveloperStates.get_group_name_state)
@router.message(F.text == 'Назад', DeveloperStates.chose_group_to_delete_state)
async def mailing_management(message: Message, state: FSMContext, config: BotConfig):
    await message.answer(text=mailing_management_text(config=config), reply_markup=MAILING_MANAGEMENT_KB)
    await state.set_state(DeveloperStates.mailing_management_state)


@router.message(F.text == 'Добавить группу', DeveloperStates.mailing_management_state)
@router.message(F.text == 'Назад', DeveloperStates.get_group_description_state)
async def add_new_mailing_group(message: Message, state: FSMContext):
    await message.answer(text=INPUT_GROUP_NAME, reply_markup=BACK_HOME_TEXT_KB)
    await state.set_state(DeveloperStates.get_group_name_state)


@router.message(DeveloperStates.get_group_name_state)
@router.message(F.text == 'Назад', DeveloperStates.add_group_state)
async def get_group_name(message: Message, state: FSMContext, config: BotConfig):
    group_name = message.text.strip()
    if group_name in config.all_groups.keys():
        await message.answer(text='Такая группа уже существует. Введите новое имя',
                             reply_markup=BACK_HOME_TEXT_KB)
        return

    await message.answer(text=input_group_description_text(group_name=group_name), reply_markup=BACK_HOME_TEXT_KB)
    await state.update_data(group_name=group_name)
    await state.set_state(DeveloperStates.get_group_description_state)


@router.message(DeveloperStates.get_group_description_state)
async def get_group_description(message: Message, state: FSMContext):
    data = await state.get_data()
    group_name = data['group_name']
    group_description = message.text.strip()
    await message.answer(text=confirm_new_group_data(group_name, group_description), reply_markup=CONTINUE_BACK_HOME_KB)
    await state.update_data(group_description=group_description)
    await state.set_state(DeveloperStates.add_group_state)


@router.message(F.text == 'Продолжить', DeveloperStates.add_group_state)
async def add_new_group(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    group_name = data['group_name']
    group_description = data['group_description']
    await config.add_mailing_group(group_name, group_description)
    await message.answer(text='Группа успешно добавлена', reply_markup=HOME_KB)
    await state.clear()


@router.message(F.text == 'Удалить группу', DeveloperStates.mailing_management_state)
@router.message(F.text == 'Назад', DeveloperStates.confirm_group_to_delete_state)
async def print_groups_to_delete(message: Message, state: FSMContext, config: BotConfig):
    await message.answer(text='\n'.join([f'{name}: {description} - {len(config.get_ids_by_mailing_group(name))} участников' for name, description in config.all_groups.items()]))
    await message.answer(text='Выберете группу для удаления',
                         reply_markup=groups_to_delete_kb(list(config.all_groups.keys())))
    await state.set_state(DeveloperStates.chose_group_to_delete_state)


@router.message(DeveloperStates.chose_group_to_delete_state)
async def confirm_group_delete(message: Message, state: FSMContext, config: BotConfig):
    group_name = message.text
    ids = config.get_ids_by_mailing_group(group_name)
    await message.answer(text=confirm_group_delete_text(group_name=group_name, users_number=len(ids)),
                         reply_markup=CONTINUE_BACK_HOME_KB)
    await state.update_data(group_name=group_name)
    await state.set_state(DeveloperStates.confirm_group_to_delete_state)


@router.message(F.text == 'Продолжить', DeveloperStates.confirm_group_to_delete_state)
async def delete_mailing_group(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    group_name = data['group_name']
    if group_name not in config.all_groups.keys():
        await message.answer(text=f'Группа {group_name} не найдена.', reply_markup=HOME_KB)
        return
    group_ids = config.get_ids_by_mailing_group(group_name)
    for c_id in group_ids:
        await config.remove_user_form_mailing_group(user_id=c_id, group=group_name)
    await config.remove_mailing_group(group_name)
    await message.answer(text=f'Группа {group_name} успешно удалена.', reply_markup=HOME_KB)
    await state.clear()
