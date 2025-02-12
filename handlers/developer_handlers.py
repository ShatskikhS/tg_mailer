from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.role_filters import RoleFilter
from project_types.enum_types import ChatRole
from project_types.bot_config import BotConfig
from keboards import developer_kb as kb
from texts import common_texts as c_texts


router = Router()


@router.message(F.text == 'Домой', RoleFilter(role=ChatRole.DEVELOPER))
async def home(message: Message, state: FSMContext, config: BotConfig):
    await state.clear()
    current_user = config.users[message.from_user.id]
    await message.answer(text=c_texts.HOME, reply_markup=kb.get_home_developer_kb(user=current_user))