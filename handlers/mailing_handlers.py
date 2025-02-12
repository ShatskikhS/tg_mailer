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
from project_types.enum_types import MailingGroup


router = Router()


@router.message(F.text == 'Рассылка', RoleFilter(role=[ChatRole.ADMIN, ChatRole.DEVELOPER]))
@router.message(F.text == 'Назад', MailingStates.GetMessageText)
async def mailing_start(message: Message, state: FSMContext):
    await message.answer(text=c_texts.MAILING_START, reply_markup=kb.MAILING_START_KB)
    await state.set_state(MailingStates.MailingStart)


@router.message(F.text == 'Выбрать группы для рассылки', MailingStates.MailingStart)
async def chose_groups(message: Message, state: FSMContext, config: BotConfig):
    options = await config.get_mailing_options()
    await message.answer_poll(question=c_texts.CHOSE_GROUPS,
                              allows_multiple_answers=True,
                              options=options,
                              reply_markup=kb.HOME_KB)
    await state.update_data(options=options)
    await state.set_state(MailingStates.PoolOptions)


@router.poll_answer(MailingStates.PoolOptions)
async def mailing_by_pool(poll_answer: PollAnswer, state: FSMContext, config: BotConfig, bot: Bot):
    data = await state.get_data()
    all_poll_options: List[str]  = data['options']
    mailing_options = poll_answer.option_ids
    print(f'{mailing_options=}')
    mailing_ids = []
    mailing_groups = []
    for option in mailing_options:
        group_name = all_poll_options[option].split(':')[0]
        mailing_groups.append(MailingGroup(group_name))
        mailing_ids.extend(config.get_ids_by_mailing_group(MailingGroup(group_name)))

    await state.update_data(mailing_ids=list(set(mailing_ids)))
    await bot.send_message(chat_id=poll_answer.user.id,
                           text=c_texts.get_input_text(groups=mailing_groups, nuber_users=len(mailing_ids)),
                           reply_markup=kb.BACK_HOME_KB)

    await state.set_state(MailingStates.GetMessageText)


@router.message(F.text == 'Отправить всем', MailingStates.MailingStart)
async def mailing_all(message: Message, state: FSMContext, config: BotConfig):
    mailing_ids = config.users.keys()
    await state.update_data(mailing_ids=mailing_ids)
    mailing_groups = [group for group in MailingGroup]

    await message.answer(text=c_texts.get_input_text(groups=mailing_groups, nuber_users=len(mailing_ids)),
                         reply_markup=kb.BACK_HOME_KB)

    await state.set_state(MailingStates.GetMessageText)


@router.message(MailingStates.GetMessageText)
async def mailing_finish(message: Message, state: FSMContext, config: BotConfig, bot: Bot):
    data = await state.get_data()
    mailing_ids = data['mailing_ids']
    mailing_text = message.text

    mailed_number = 0
    mailing_fails = []
    for mailing_id in mailing_ids:
        mailing_user = config.users[mailing_id]
        if mailing_user.is_subscribed and not mailing_user.is_bot:
            try:
                await bot.send_message(chat_id=mailing_id, text=mailing_text)
                mailed_number += 1
            except Exception as error:
                mailing_fails.append(f'User: {mailing_user.full_name}, exception: {error}')

    answer_texts = split_message(c_texts.mailing_result(mailed_number, mailing_fails))
    for answer_text in answer_texts:
        await message.answer(text=answer_text, reply_markup=kb.HOME_KB)
