import os
from dotenv import load_dotenv

from sqlalchemy.engine.url import URL


load_dotenv()

DATABASE_URL = URL.create(
    drivername=f'{os.getenv("DB_NAME")}+{os.getenv("DB_DRIVER")}',
    database=os.getenv("DB_PATH")
)

DEVELOPER_IDS = [int(value) for value in os.getenv("DEVELOPER_IDS").split(",")]

BOT_TOKEN = os.getenv("BOT_TOKEN")
MESSAGE_MAX_LENGTH = int(os.getenv("MESSAGE_MAX_LENGTH"))

COMMUNITY_NAME = os.getenv("COMMUNITY_NAME")

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
