import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, DATABASE_URL
from project_types import BotConfig
from db import DatabaseManager

from handlers.new_user import router as new_user_router


db = DatabaseManager(DATABASE_URL)
config = BotConfig(db=db)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(config=config)

dp.include_routers(new_user_router)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await db.init_db()
    await config.read_users()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
