from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.role_filters import RoleFilter
from keboards import user_kb as kb
from project_types.enum_types import ChatRole
from project_types.bot_config import BotConfig
from texts import user_texts as texts
from texts.text_methods import split_message
from fsms import UserStates

router = Router()

@router.message(F.text == 'Домой', RoleFilter(role=ChatRole.USER))
@router.message(F.text == 'Назад', UserStates.Feedback)
async def home(message: Message, config: BotConfig, state: FSMContext) -> None:
    await state.clear()
    await message.answer(text=texts.HOME,
                         reply_markup=kb.get_hone_usr_kb(user=config.ger_user_by_id(user_id=message.from_user.id)))

@router.message(F.text == 'Справка', RoleFilter(role=ChatRole.USER))
async def help_msg(message: Message, config: BotConfig) -> None:
    await message.answer(text=texts.get_help_text(user=config.ger_user_by_id(user_id=message.from_user.id)),
                         reply_markup=kb.get_hone_usr_kb(user=config.ger_user_by_id(user_id=message.from_user.id)))


@router.message(F.text == 'Написать администраторам', RoleFilter(role=ChatRole.USER))
async def user_feedback(message: Message, state: FSMContext) -> None:
    await message.answer(text=texts.FEEDBACK, reply_markup=kb.FEEDBACK_KB)
    await state.set_state(UserStates.Feedback)


@router.message(UserStates.Feedback)
async def send_feedback(message: Message, state: FSMContext, config: BotConfig, bot: Bot) -> None:
    current_user = config.ger_user_by_id(user_id=message.from_user.id)
    mailing_ids = config.get_ids_by_role(ChatRole.DEVELOPER)
    mailing_ids.extend(config.get_ids_by_role(ChatRole.ADMIN))

    text = (f'Сообщение от {current_user.full_name()}:\n'
            f'{message.text}')
    mailing_text = split_message(text)

    for current_id in mailing_ids:
        for current_text in mailing_text:
            await bot.send_message(chat_id=current_id, text=current_text)

    await message.answer(text=texts.MESSAGE_SENT, reply_markup=kb.get_hone_usr_kb(user=current_user))
    await state.clear()