from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.enums import ParseMode, ChatAction

from filters.role_filters import NonUserFilter
from keboards import common as common_kb
from fsms import NewUserStates as States
from texts import new_user as texts
from project_types import BotConfig, UserType, ChatRole

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
        pass

    await state.clear()
