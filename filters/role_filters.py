from aiogram.filters import BaseFilter
from aiogram.types import Message

from project_types import BotConfig


class NonUserFilter(BaseFilter):
    async def __call__(self, message: Message, config: BotConfig):
        return message.from_user.id not in config.users.keys()
