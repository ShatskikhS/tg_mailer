from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message

from project_types.bot_config import BotConfig
from project_types.enum_types import ChatRole


class NonUserFilter(BaseFilter):
    async def __call__(self, message: Message, config: BotConfig):
        return message.from_user.id not in config.users.keys()


class RoleFilter(BaseFilter):
    def __init__(self, role: List[ChatRole] | ChatRole):
        self.role = role

    async def __call__(self, message: Message, config: BotConfig):
        user_role = config.get_role_by_id(user_id=message.from_user.id)
        if isinstance(self.role, ChatRole):
            return self.role == user_role
        else:
            return user_role in self.role
