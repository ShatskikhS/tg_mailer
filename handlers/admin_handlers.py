from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.role_filters import RoleFilter
from project_types.enum_types import ChatRole, NoticeAction
from project_types.bot_config import BotConfig
from keboards import admin_kb as kb
from keboards.common_kb import HOME_KB
from keboards.inline_kb import NewUserNotice
from texts.common_texts import HOME, APPLICANT_NOTICE_APPROVED, APPLICANT_NOTICE_DECLINED, APPLICANT_NOTICE_POSTPONED
from texts.new_user import APPLICANT_APPROVED, APPLICANT_DECLINED


router = Router()

@router.message(F.text == 'Домой', RoleFilter(role=ChatRole.ADMIN))
async def home(message: Message, config: BotConfig, state: FSMContext):
    await state.clear()
    current_user = config.users[message.from_user.id]
    await message.answer(text= HOME, reply_markup=kb.get_home_admin_kb(current_user))


@router.callback_query(NewUserNotice.filter())
async def new_app_notice(callback_query: CallbackQuery, callback_data:NewUserNotice, config: BotConfig, bot: Bot):
    if callback_data.action == NoticeAction.APPROVE:
        await config.change_subscriptions(user_id=callback_data.user_id)
        await config.alter_user_role(user_id=callback_data.user_id, new_role=ChatRole.USER)
        await bot.send_message(chat_id=callback_data.user_id, text=APPLICANT_APPROVED, reply_markup=HOME_KB)
        await callback_query.answer(text=APPLICANT_NOTICE_APPROVED)
    if callback_data.action == NoticeAction.DECLINE:
        c_info = await config.get_user_info(user_id=callback_data.user_id)
        if c_info is not None:
            await config.remove_user_info(user_id=callback_data.user_id)
        await config.remove_user_by_id(user_id=callback_data.user_id)
        await bot.send_message(chat_id=callback_data.user_id, text=APPLICANT_DECLINED)
        await callback_query.answer(text=APPLICANT_NOTICE_DECLINED)
    if callback_data.action == NoticeAction.POSTPONE:
        await callback_query.answer(text=callback_query.message.text)
        await callback_query.message.delete()
        await callback_query.answer(text=APPLICANT_NOTICE_POSTPONED)


