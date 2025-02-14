from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from filters.role_filters import NonUserFilter
from fsms import NewUserStates as States
from keboards import common_kb as common_kb
from keboards.inline_kb import get_new_app_notice_kb
from project_types.enum_types import ChatRole
from project_types.user_type import UserType
from project_types.bot_config import BotConfig
from texts import new_user as texts
from texts.text_methods import split_message


router = Router()

@router.message(CommandStart(), NonUserFilter())
async def home(message: Message, state: FSMContext) -> None:
    await message.answer(text=texts.NEW_USER_GREETINGS, reply_markup=common_kb.PROCEED_KB)
    await state.set_state(States.HomeState)


@router.message(F.text == 'Продолжить', States.HomeState)
@router.message(F.text == 'Назад', States.ConfirmInfo)
async def get_user_info(message: Message, state: FSMContext, config: BotConfig) -> None:
    if message.from_user.id not in config.developer_ids:
        await message.answer(text=texts.GET_USER_INFO_TEXT, reply_markup=common_kb.GET_NEW_USER_INFO_KB)
        await state.set_state(States.GetInfo)
    else:
        await config.add_user(user=UserType(user=message.from_user, role=ChatRole.DEVELOPER))
        await message.answer(text=texts.NEW_DEVELOPER, reply_markup=common_kb.HOME_KB)
        await state.clear()


@router.message(States.GetInfo)
async def confirm_info(message: Message, state: FSMContext) -> None:
    if message.text == 'Не хочу представляться':
        await message.answer(text='Вы не предоставили информацию о себе.')
    else:
        await message.answer(text='Администраторам будет передана следующая информация:')
        await message.answer(text=message.text)
        await state.update_data(user_info = message.text)
    await message.answer(text=texts.CONFIRM_INFO_TEXT, reply_markup=common_kb.BACK_SEND_KB)
    await state.set_state(States.ConfirmInfo)


@router.message(F.text == 'Отправить', States.ConfirmInfo)
async def new_user_finish(message: Message, state: FSMContext, config: BotConfig, bot: Bot) -> None:
    state_data = await state.get_data()
    user_info = state_data.get('user_info')
    new_user = UserType(user=message.from_user)

    await config.add_user(user=new_user)
    if user_info is not None:
        await config.add_user_info(user_id=new_user.id, user_info=user_info)

    ids = config.get_ids_by_role(role=ChatRole.ADMIN)
    ids.extend(config.get_ids_by_role(role=ChatRole.DEVELOPER))
    notification_text = texts.new_app_notification(user=new_user, user_info=user_info)
    notification_texts = split_message(notification_text)
    for current_id in ids:
        for current_text in notification_texts:
            await bot.send_message(chat_id=current_id,
                                   text=current_text,
                                   reply_markup=get_new_app_notice_kb(user_id=new_user.id, user_info=user_info))

    await message.answer(text=texts.APPLICATION_ACCEPTED, reply_markup=ReplyKeyboardRemove())
    await state.clear()
