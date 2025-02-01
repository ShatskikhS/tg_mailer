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
