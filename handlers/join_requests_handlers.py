from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from filters.role_filters import RoleFilter
from project_types.bot_config import BotConfig
from keboards.common_kb import get_applicants_kb, HOME_KB
from texts.new_user import current_app_notification
from texts.common_texts import APPLICANT_NOTICE_APPROVED, APPLICANT_NOTICE_DECLINED
from texts.new_user import APPLICANT_DECLINED, APPLICANT_APPROVED
from project_types.enum_types import ChatRole
from fsms import ApplicationsStates


router = Router()


@router.message(F.text == 'Запросы на вступление', RoleFilter(role=[ChatRole.ADMIN, ChatRole.DEVELOPER]))
@router.message(F.text == 'Предыдущее', ApplicationsStates.CurrentApplicant)
@router.message(F.text == 'Следующее', ApplicationsStates.CurrentApplicant)
@router.message(F.text == 'Отклонить', ApplicationsStates.CurrentApplicant)
@router.message(F.text == 'Одобрить', ApplicationsStates.CurrentApplicant)
async def join_requests(message: Message, state: FSMContext, config: BotConfig, bot: Bot):
    applicant_ids = config.get_ids_by_role(ChatRole.APPLICANT)
    if len(applicant_ids) == 0:
        await message.answer(text='Нет открытых заявок на вступление.', reply_markup=HOME_KB)
    else:
        state_data = await state.get_data()
        try:
            prev_user_number = state_data['prev_user_number']
            prev_id = state_data['prev_id']
            if message.text == 'Предыдущее':
                user_number = prev_user_number - 1
            elif message.text == 'Следующее':
                user_number = prev_user_number + 1
            elif message.text == 'Отклонить':
                user_number = prev_user_number
                u_info = await config.get_user_info(user_id=prev_user_number)
                if u_info is not None:
                    await config.remove_user_info(user_id=prev_user_number)
                await config.remove_user_by_id(user_id=prev_id)
                await message.answer(text=APPLICANT_NOTICE_DECLINED)
                await bot.send_message(chat_id=prev_id, text=APPLICANT_DECLINED)
            elif message.text == 'Одобрить':
                user_number = prev_user_number
                await config.alter_user_role(user_id=prev_id, new_role=ChatRole.USER)
                await message.answer(text=APPLICANT_NOTICE_APPROVED)
                await bot.send_message(chat_id=prev_id, text=APPLICANT_APPROVED, reply_markup=HOME_KB)
            else:
                user_number = 0
            user_id = applicant_ids[user_number]
        except Exception as ex:
            print(f'Current user not found: {ex}')
            user_number = 0
            user_id = applicant_ids[user_number]

        back_btn: bool = user_number > 0
        fwd_btn: bool = user_number < len(applicant_ids) - 1
        user_info = await config.get_user_info(user_id=user_id)
        kb = get_applicants_kb(back_button=back_btn, front_button=fwd_btn)
        text = current_app_notification(user=config.users[user_id], user_info=user_info,
                                        user_number=user_number + 1, total=len(applicant_ids))

        await message.answer(text=text , reply_markup=kb)

        await state.update_data(prev_user_number=user_number, prev_id = user_id)
        await state.set_state(ApplicationsStates.CurrentApplicant)
