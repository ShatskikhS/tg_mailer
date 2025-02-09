import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data import BOT_TOKEN, DATABASE_URL
from project_types.bot_config import BotConfig
from db.raw_sql import RawSQL

from handlers.new_user import router as new_user_router


db_manager = RawSQL(DATABASE_URL)
config = BotConfig(db_manager=db_manager)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(config=config)

dp.include_routers(new_user_router)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await config.init_config()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
