from aiogram import Router, F
from aiogram.types import Message

from filters.role_filters import RoleFilter
from keboards.user_kb import get_hone_usr_kb
from project_types import ChatRole, BotConfig

router = Router()

@router.message(F.text == 'Подписаться на рассылку',
                RoleFilter(role=[ChatRole.ADMIN, ChatRole.DEVELOPER, ChatRole.USER]))
@router.message(F.text == 'Отписаться от рассылки',
                RoleFilter(role=[ChatRole.ADMIN, ChatRole.DEVELOPER, ChatRole.USER]))
async def subscriptions(message: Message, config: BotConfig):
    is_subscribed = await config.change_subscriptions(user_id=message.from_user.id)
    current_user = config.ger_user_by_id(user_id=message.from_user.id)
    text = 'Вы подписались на рассылку' if is_subscribed else 'Вы отписались от рассылки'

    if current_user.role == ChatRole.USER:
        await message.answer(text=text, reply_markup=get_hone_usr_kb(user=current_user))
    elif current_user.role == ChatRole.ADMIN:
        # TODO: complete block admin_home_kb is completed
        pass
    elif current_user.role == ChatRole.DEVELOPER:
        # TODO: complete block developer_home_kb is completed
        pass
