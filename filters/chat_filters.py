from aiogram.filters import BaseFilter
from aiogram.types import Message

from project_types import BotConfig


class BotChatFilter(BaseFilter):
    async def __call__(self, message: Message, config: BotConfig) -> bool:
        return message.chat.id == config.bot_id