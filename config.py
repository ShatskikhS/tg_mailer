import os
from dotenv import load_dotenv

from sqlalchemy.engine.url import URL

from project_types import ChatRole


load_dotenv()

DATABASE_URL = URL.create(
    drivername=f'{os.getenv("DB_NAME")}+{os.getenv("DB_DRIVER")}',
    database=os.getenv("DB_PATH")
)

DEFAULT_ROLE = ChatRole(os.getenv("DEFAULT_ROLE_NAME"))
DEVELOPER_IDS = [int(value) for value in os.getenv("DEVELOPER_IDS").split(",")]

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ID = os.getenv("BOT_ID")

COMMUNITY_NAME = os.getenv("COMMUNITY_NAME")

DT_FORMAT = '%Y-%m-%d %H:%M:%S'