from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config_data import DATETIME_FORMAT
from filters.role_filters import RoleFilter
from fsms import NewUserStates
from keboards import admin_kb as kb
from keboards.common_kb import HOME_KB, ADD_TO_GROUP_HOME_KB, EDIT_GROUPS_HOME, edit_groups_builder_kb
from keboards.inline_kb import NewUserNotice
from project_types.bot_config import BotConfig
from project_types.enum_types import ChatRole, NoticeAction
from texts.common_texts import (HOME, APPLICANT_NOTICE_DECLINED, APPLICANT_NOTICE_POSTPONED, NEW_APPLICANT_APPROVED,
                                applicant_declined_text, applicant_approved_text)
from texts.new_user import APPLICANT_APPROVED, APPLICANT_DECLINED

router = Router()

@router.message(F.text == 'Домой', RoleFilter(role=ChatRole.ADMIN))
async def home(message: Message, config: BotConfig, state: FSMContext):
    await state.clear()
    current_user = config.users[message.from_user.id]
    await message.answer(text= HOME, reply_markup=kb.get_home_admin_kb(current_user))


@router.callback_query(NewUserNotice.filter())
async def new_app_notice(callback_query: CallbackQuery, callback_data: NewUserNotice,
                         config: BotConfig, bot: Bot, state: FSMContext):
    user = config.users.get(callback_data.user_id)
    admin = config.users.get(callback_query.from_user.id)
    m_app = await config.get_application(applicant_id=callback_data.user_id)
    if user is not None and user.role == ChatRole.APPLICANT:
        if callback_data.action == NoticeAction.APPROVE:
            # Add new user to the bot
            await config.change_subscriptions(user_id=user.id)
            await config.alter_user_role(user_id=user.id, new_role=ChatRole.USER)
            await config.close_application(applicant_id=user.id, admin_id=admin.id)
            await bot.send_message(chat_id=user.id, text=APPLICANT_APPROVED, reply_markup=HOME_KB)

            # Offer admin to add new user to mailing groups
            await bot.send_message(chat_id=admin.id,
                                   text= NEW_APPLICANT_APPROVED,
                                   reply_markup=ADD_TO_GROUP_HOME_KB)
            await state.set_state(NewUserStates.add_to_group)
            await state.update_data(user_id=user.id)
        if callback_data.action == NoticeAction.DECLINE:
            await config.remove_user_by_id(user_id=user.id)
            await config.close_application(applicant_id=user.id, admin_id=admin.id)
            await bot.send_message(chat_id=user.id, text=APPLICANT_DECLINED)
            await callback_query.answer(text=APPLICANT_NOTICE_DECLINED)
        if callback_data.action == NoticeAction.POSTPONE:
            await callback_query.answer(text=callback_query.message.text)
            await callback_query.message.delete()
            await callback_query.answer(text=APPLICANT_NOTICE_POSTPONED)
    elif user is None:
        await callback_query.answer(text=applicant_declined_text(amin_name=admin.full_name(),
                                                                date=m_app.decision_date.strftime(DATETIME_FORMAT)))
    else:
        await callback_query.answer(text=applicant_approved_text(amin_name=admin.full_name(),
                                                                date=m_app.decision_date.strftime(DATETIME_FORMAT)))


@router.message(F.text == 'Добавить в группу', NewUserStates.add_to_group)
@router.message(F.text == 'Редактировать группы пользователя', NewUserStates.add_to_group)
async def chose_group(message: Message, config: BotConfig, state: FSMContext):
    data = await state.get_data()
    user = config.users[data['user_id']]
    await message.answer(text='Выберите группу',
                         reply_markup=edit_groups_builder_kb(user=user, all_groups=list(config.all_groups.keys()), back=False))
    await state.set_state(NewUserStates.chose_group)


@router.message(F.text != 'Домой', NewUserStates.chose_group)
async def add_user_to_group(message: Message, config: BotConfig, state: FSMContext):
    data = await state.get_data()
    user = config.users[data['user_id']]
    group = message.text.replace('Добавить в ', '').replace('Удалить из ', '')
    if message.text.startswith('Добавить в '):
        await config.add_user_to_mailing_group(user.id, group)
        await message.answer(text=user.represent_user_full())
        await message.answer(text=f'Пользователь {user.full_name()} успешно добавлен в группу {group}',
                             reply_markup=EDIT_GROUPS_HOME)
    elif message.text.startswith('Удалить из '):
        await config.remove_user_form_mailing_group(user_id=user.id, group=group)
        await message.answer(text=user.represent_user_full())
        await message.answer(text=f'Пользователь {user.full_name()} удален из группы {group}',
                             reply_markup=EDIT_GROUPS_HOME)
    else:
        await message.answer(text='Воспользуйтесь кнопками 🤦‍♂️')
        return
    await state.set_state(NewUserStates.add_to_group)



