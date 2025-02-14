import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data import BOT_TOKEN, DATABASE_URL
from project_types.bot_config import BotConfig
from db.raw_sql import RawSQL

from handlers.new_user import router as new_user_router
from handlers.user_handlers import router as user_router
from handlers.admin_handlers import router as admin_router
from handlers.mailing_handlers import router as mailing_router
from handlers.developer_handlers import router as developer_router
from handlers.join_requests_handlers import router as join_requests_router


db_manager = RawSQL(DATABASE_URL)
config = BotConfig(db_manager=db_manager)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(config=config)

dp.include_routers(new_user_router,
                   user_router,
                   admin_router,
                   developer_router,
                   mailing_router,
                   join_requests_router)

async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    await config.init_config()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
