from typing import List

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PollAnswer

from filters.role_filters import RoleFilter
from project_types.enum_types import ChatRole
from project_types.bot_config import BotConfig
from keboards import common_kb as kb
from texts import common_texts as c_texts
from texts.text_methods import split_message
from fsms import MailingStates


router = Router()


@router.message(F.text == 'Рассылка', RoleFilter(role=[ChatRole.ADMIN, ChatRole.DEVELOPER]))
@router.message(F.text == 'Назад', MailingStates.get_message_text)
@router.message(F.text == 'Назад', MailingStates.group_buttons)
async def mailing_start(message: Message, state: FSMContext):
    await message.answer(text=c_texts.MAILING_START, reply_markup=kb.MAILING_START_KB)
    await state.set_state(MailingStates.mailing_start)


@router.message(F.text == 'Выбрать группы', RoleFilter(role=[ChatRole.ADMIN, ChatRole.DEVELOPER]))
@router.message(~F.text.in_({'Назад', 'Получатели', 'Продолжить', 'Домой'}), MailingStates.group_buttons)
@router.message(F.text == 'Назад', MailingStates.recipients)
async def show_groups(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    groups = data.get('groups') or []
    current_group = message.text.replace('✅ ', '').replace('⬜ ', '')
    if current_group in config.all_groups.keys():
        if current_group in groups:
            groups.remove(current_group)
        else:
            groups.append(current_group)

    for text in split_message(c_texts.chose_groups_text(config, groups)):
        await message.answer(text=text, reply_markup=kb.mailing_groups_builder_kb(config, groups))

    await state.update_data(groups=groups)
    await state.set_state(MailingStates.group_buttons)


@router.message(F.text == 'Получатели', MailingStates.group_buttons)
async def show_recipients(message: Message, state: FSMContext, config: BotConfig):
    data = await state.get_data()
    groups: List[str] = data['groups']
    text = c_texts.show_recipients_text(groups, config)
    msg_texts = split_message(text)
    for msg_text in msg_texts:
        await message.answer(text=msg_text, reply_markup=kb.CONTINUE_BACK_HOME_KB)
    await state.set_state(MailingStates.recipients)


@router.message(F.text == 'Выбрать группы для рассылки', MailingStates.mailing_start)
async def chose_groups(message: Message, state: FSMContext, config: BotConfig):
    options = [f"{group_name}: {group_description}" for group_name, group_description in config.all_groups.items()]
    await message.answer_poll(question=c_texts.CHOSE_GROUPS,
                              allows_multiple_answers=True,
                              options=options,
                              is_anonymous=False,
                              reply_markup=kb.HOME_KB)
    await state.update_data(options=options)
    await state.set_state(MailingStates.pool_options)


@router.poll_answer(MailingStates.pool_options)
async def mailing_by_pool(poll_answer: PollAnswer, state: FSMContext, config: BotConfig, bot: Bot):
    data = await state.get_data()
    all_poll_options: List[str]  = data['options']
    mailing_options = poll_answer.option_ids
    mailing_groups: List[str] = []
    for option in mailing_options:
        group_name = all_poll_options[option].split(':')[0]
        mailing_groups.append(group_name)

    await state.update_data(groups=mailing_groups)
    await bot.send_message(chat_id=poll_answer.user.id,
                           text=c_texts.get_input_text(groups=mailing_groups,
                                                       nuber_users=len(config.get_mailing_ids(mailing_groups))),
                           reply_markup=kb.BACK_HOME_KB)

    await state.set_state(MailingStates.get_message_text)


@router.message(F.text == 'Отправить всем', MailingStates.mailing_start)
@router.message(F.text == 'Продолжить', MailingStates.group_buttons)
@router.message(F.text == 'Продолжить', MailingStates.recipients)
async def mailing_all(message: Message, state: FSMContext, config: BotConfig):
    if message.text == 'Отправить всем':
        groups = list(config.all_groups.keys())
        await state.update_data(groups=groups)
    else:
        data = await state.get_data()
        groups = data['groups']
    await message.answer(text=c_texts.get_input_text(groups=groups,
                                                     nuber_users=len(config.get_mailing_ids(groups))),
                         reply_markup=kb.BACK_HOME_KB)

    await state.set_state(MailingStates.get_message_text)


@router.message(MailingStates.get_message_text)
async def mailing_finish(message: Message, state: FSMContext, config: BotConfig, bot: Bot):
    data = await state.get_data()
    groups = data.get('groups')
    mailing_ids = config.get_mailing_ids(groups)
    mailing_text = message.text

    mailed_number = 0
    mailing_fails = []
    for mailing_id in mailing_ids:
        try:
            await bot.send_message(chat_id=mailing_id, text=mailing_text)
            mailed_number += 1
        except Exception as e:
            mailing_fails.append(f'User: {config.users[mailing_id].full_name()} Exception: {e}')

    answer_texts = split_message(text=c_texts.mailing_result(mailed_number, mailing_fails))
    for answer_text in answer_texts:
        await message.answer(text=answer_text, reply_markup=kb.HOME_KB)

    await state.clear()
