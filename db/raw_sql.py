from typing import Dict, List
from datetime import datetime

from sqlalchemy.ext.asyncio import create_async_engine

from config_data import DATABASE_URL
from project_types.enum_types import ChatRole
from project_types.user_type import UserType
from db.sql_clauses import *


class RawSQL:
    def __init__(self, url: str = DATABASE_URL):
        self.engine = create_async_engine(url, echo=True)

    async def init_db (self) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(CREATE_MAILING_GROUPS_TABLE)
            await conn.execute(CREATE_CHAT_ROLES_TABLE)
            await conn.execute(CREATE_USERS_TABLE)
            await conn.execute(CREATE_USERS_MAILING_GROUPS_TABLE)
            await conn.execute(CREATE_APPLICATIONS_TABLE)
            await conn.execute(CREATE_APPLICANTS_NOTIFIED_ADMINS_TABLE)
            result = await conn.execute(SELECT_ROLES_NUMBER)
            if result.scalar() == 0:
                for role in ChatRole:
                    await self.add_chat_role(role)

    async def get_all_mailing_groups(self) -> Dict[str, str]:
        async with self.engine.connect() as conn:
            is_exists = await conn.execute(EXISTS_MAILING_GROUPS)
            if is_exists.scalar() == 0:
                return {}
            data = await conn.execute(SELECT_ALL_MAILING_GROUPS)
        return {row[0]: row[1] for row in data.all()}

    async def add_applicant(self, applicant_id: int, user_info: str | None = None) -> None:
        async with self.engine.begin() as conn:
            if user_info is not None:
                await conn.execute(ADD_APPLICATION_INFO, {'applicant_id': applicant_id, 'applicant_info': user_info})
            else:
                await conn.execute(ADD_APPLICATION, {'applicant_id': applicant_id})

    async def close_application(self, applicant_id: int, admin_id: int) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(CLOSE_APPLICATION, {'applicant_id': applicant_id,
                                                   'admin_id': admin_id,
                                                   'close_date': datetime.now()})

    async def add_notified_admin(self, applicant_id: int, admin_id: int, message_id: int) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(ADD_NOTIFIED_ADMIN, {'applicant_id': applicant_id,
                                                    'admin_id': admin_id,
                                                    'message_id': message_id})

    async def get_notified_admins(self, applicant_id: int) -> List[int]:
        async with self.engine.begin() as conn:
            result = await conn.execute(GET_NOTIFIED_ADMINS, {'applicant_id': applicant_id})
        return list(result.scalars())

    async def get_application(self, applicant_id: int):
        async with self.engine.begin() as conn:
            row = await conn.execute(GET_APPLICATION, {'applicant_id': applicant_id})
            return row.one()

    async def delete_notified_admins(self, applicant_id: int) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(DELETE_NOTIFIED_ADMINS, {'applicant_id': applicant_id})

    async def get_user_info(self, user_id: int) -> str:
        async with self.engine.begin() as conn:
            result = await conn.execute(GET_USER_INFO, {'user_id': user_id})
        return result.scalar()

    async def add_mailing_group(self, mailing_group: str, group_description: str | None = None) -> None:
        async with self.engine.begin() as conn:
            if group_description is None:
                await conn.execute(ADD_GROUP_NAME, {'group_name': mailing_group})
            else:
                await conn.execute(ADD_GROUP_NAME_DESCRIPTION, {'group_name': mailing_group, 'group_description': group_description})

    async def delete_mailing_group(self, mailing_group: str) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(DELETE_GROUP, {'group_name': mailing_group})

    async def add_chat_role(self, chat_role: ChatRole, role_description: str | None = None)  -> None:
        async with self.engine.begin() as conn:
            if role_description is None:
                await conn.execute(ADD_CHAT_ROLE, {'chat_role': chat_role.value})
            else:
                await conn.execute(ADD_CHAT_ROLE_DESCRIPTION,
                                   {'chat_role': chat_role.value, 'role_description': role_description})

    async def add_user_to_mailing_group(self, user_id: int, mailing_group: str):
        async with self.engine.begin() as conn:
            await conn.execute(ADD_USER_TO_MAILING_GROUP, {'user_id': user_id, 'group_name': mailing_group})

    async def add_user(self, user: UserType):
        async with self.engine.begin() as conn:
            await conn.execute(ADD_USER, user.to_db_params())

    async def update_user_subscription(self, user_id: int, is_subscribed: bool) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(UPDATE_SUBSCRIPTION, {'user_id': user_id, 'is_subscribed': is_subscribed})

    async def get_all_users(self) -> Dict[int, UserType]:
        async with self.engine.begin() as conn:
            result = await conn.execute(SELECT_ALL_USERS)
        all_users = {}
        for current_row in result.mappings():
            all_users[current_row['user_id']] = UserType.from_dict(data=current_row)

        for user_id, user in all_users.items():
            groups = await self.get_user_groups(user_id)
            user.groups = groups
        return all_users

    async def get_user_groups(self, user_id: int)-> List[str]:
        async with self.engine.begin() as conn:
            result = await conn.execute(SELECT_USER_GROUPS, {'user_id': user_id})
        return list(result.scalars())

    async def remove_user_from_mailing_group(self, user_id: int, mailing_group: str) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(REMOVE_USER_FROM_MAILING_GROUP, {'user_id': user_id, 'group_name': mailing_group})

    async def remove_user(self, user_id: int) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(DELETE_USER, {'user_id': user_id})

    async def update_user_role(self, user_id: int, new_role: ChatRole) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(UPDATE_USER_ROLE, {'user_id': user_id, 'role_name': new_role.value})
