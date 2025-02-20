from aiogram import Router, F
from aiogram.types import Message

from filters.role_filters import RoleFilter
from keboards.user_kb import get_hone_usr_kb
from keboards.admin_kb import get_home_admin_kb
from keboards.developer_kb import home_developer_kb
from project_types.enum_types import ChatRole
from project_types.bot_config import BotConfig

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
        await message.answer(text=text, reply_markup=get_home_admin_kb(user=current_user))
    elif current_user.role == ChatRole.DEVELOPER:
        await message.answer(text=text, reply_markup=home_developer_kb(user=current_user))
