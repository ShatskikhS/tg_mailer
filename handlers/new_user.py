from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from filters.role_filters import NonUserFilter
from fsms import NewUserStates as States
from keboards import common_kb as common_kb
from project_types.enum_types import ChatRole
from project_types.user_type import UserType
from project_types.bot_config import BotConfig
from texts import new_user as texts


router = Router()

@router.message(CommandStart(), NonUserFilter())
async def home(message: Message, state: FSMContext) -> None:
    await message.answer(text=texts.NEW_USER_GREETINGS, reply_markup=common_kb.PROCEED_KB)
    await state.set_state(States.HomeState)


@router.message(F.text == 'Продолжить', States.HomeState)
async def add_applicant(message: Message, state: FSMContext, bot: Bot, config: BotConfig) -> None:
    if message.from_user.id not in config.developer_ids:
        await message.answer(text=texts.APPLICATION_ACCEPTED, reply_markup=ReplyKeyboardRemove())
        new_user = UserType(user=message.from_user)
        await config.add_user(user=new_user)
        ids = config.get_ids_by_role(role=ChatRole.ADMIN)
        ids.extend(config.get_ids_by_role(role=ChatRole.DEVELOPER))
        for current_id in ids:
            await bot.send_message(chat_id=current_id, text=texts.new_app_notification(user=new_user))
    else:
        await config.add_user(user=UserType(user=message.from_user, role=ChatRole.DEVELOPER))
        await message.answer(text=texts.NEW_DEVELOPER, reply_markup=common_kb.PROCEED_KB)

    await state.clear()
