import os
from dotenv import load_dotenv

from sqlalchemy.engine.url import URL


load_dotenv()

DATABASE_URL = URL.create(
    drivername=f'{os.getenv("DB_NAME")}+{os.getenv("DB_DRIVER")}',
    database=os.getenv("DB_PATH")
)

DEVELOPER_IDS = [int(value) for value in os.getenv("DEVELOPER_IDS").split(",")]
role_names = os.getenv("ROLE_NAMES").split(",")
role_descriptions = os.getenv("ROLE_DESCRIPTIONS").split(",")
DEFAULT_ROLES = {role_names[i]: role_descriptions[i] if i < len(role_descriptions) else None for i in range(len(role_names))}
group_names = os.getenv("GROUP_NAMES").split(",")
group_descriptions = os.getenv("GROUP_DESCRIPTIONS").split(",")
DEFAULT_GROUPS = {group_names[i]: group_descriptions[i] if i < len(group_descriptions) else None for i in range(len(group_names))}

BOT_TOKEN = os.getenv("BOT_TOKEN")
MESSAGE_MAX_LENGTH = int(os.getenv("MESSAGE_MAX_LENGTH"))

COMMUNITY_NAME = os.getenv("COMMUNITY_NAME")

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
