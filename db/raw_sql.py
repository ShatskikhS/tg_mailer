from typing import Dict, List

from sqlalchemy.ext.asyncio import create_async_engine

from config_data import DATABASE_URL
from project_types.enum_types import ChatRole, MailingGroup
from project_types.user_type import UserType
from db.sql_clauses import (CREATE_MAILING_GROUPS_TABLE,
                            CREATE_CHAT_ROLES_TABLE,
                            CREATE_USERS_TABLE,
                            CREATE_USERS_MAILING_GROUPS_TABLE,
                            ADD_GROUP_NAME,
                            ADD_GROUP_NAME_DESCRIPTION,
                            DELETE_GROUP,
                            SELECT_GROUP_DESCRIPTION,
                            ADD_CHAT_ROLE_DESCRIPTION,
                            ADD_CHAT_ROLE,
                            SELECT_ROLE_DESCRIPTION,
                            ADD_USER,
                            ADD_USER_TO_MAILING_GROUP,
                            SELECT_ROLES_NUMBER,
                            UPDATE_SUBSCRIPTION,
                            SELECT_ALL_USERS,
                            SELECT_USER_GROUPS,
                            SELECT_USER_BY_ID,
                            REMOVE_USER_FROM_MAILING_GROUP,
                            DELETE_USER,
                            UPDATE_USER_ROLE)


class RawSQL:
    def __init__(self, url: str = DATABASE_URL):
        self.engine = create_async_engine(url, echo=True)

    async def init_db (self) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(CREATE_MAILING_GROUPS_TABLE)
            await conn.execute(CREATE_CHAT_ROLES_TABLE)
            await conn.execute(CREATE_USERS_TABLE)
            await conn.execute(CREATE_USERS_MAILING_GROUPS_TABLE)
            result = await conn.execute(SELECT_ROLES_NUMBER)
            if result.scalar() == 0:
                for role in ChatRole:
                    await self.add_chat_role(role)


    async def add_mailing_group(self, mailing_group: MailingGroup, group_description: str | None = None) -> None:
        async with self.engine.begin() as conn:
            if group_description is None:
                await conn.execute(ADD_GROUP_NAME, {'group_name': mailing_group.value})
            else:
                await conn.execute(ADD_GROUP_NAME_DESCRIPTION, {'group_name': mailing_group.value, 'group_description': group_description})

    async def delete_mailing_group(self, mailing_group: MailingGroup) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(DELETE_GROUP, {'group_name': mailing_group.value})

    async def get_group_description(self, mailing_group: MailingGroup) -> str:
        async with self.engine.begin() as conn:
            result = await conn.execute(SELECT_GROUP_DESCRIPTION, {'group_name': mailing_group.value})
        return result.scalar()

    async def add_chat_role(self, chat_role: ChatRole, role_description: str | None = None)  -> None:
        async with self.engine.begin() as conn:
            if role_description is None:
                await conn.execute(ADD_CHAT_ROLE, {'chat_role': chat_role.value})
            else:
                await conn.execute(ADD_CHAT_ROLE_DESCRIPTION,
                                   {'chat_role': chat_role.value, 'role_description': role_description})

    async def get_chat_role_description(self, chat_role: ChatRole) -> str:
        async with self.engine.begin() as conn:
            result = conn.execute(SELECT_ROLE_DESCRIPTION, {'chat_role': chat_role.value})
        return result.scalar()

    async def add_user_to_mailing_group(self, user_id: int, mailing_group: MailingGroup):
        async with self.engine.begin() as conn:
            await conn.execute(ADD_USER_TO_MAILING_GROUP, {'user_id': user_id, 'group_name': mailing_group.value})

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

    async def get_user_by_id(self, user_id: int) -> UserType:
        async with self.engine.begin() as conn:
            result = await conn.execute(SELECT_USER_BY_ID, {'user_id': user_id})
        user = UserType.from_dict(data=next(result.mappings()))
        user.groups = await self.get_user_groups(user_id)
        return user

    async def get_user_groups(self, user_id: int)-> List[MailingGroup]:
        async with self.engine.begin() as conn:
            result = await conn.execute(SELECT_USER_GROUPS, {'user_id': user_id})
        return [MailingGroup(item) for item in result.scalars()]

    async def remove_user_from_mailing_group(self, user_id: int, mailing_group: MailingGroup) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(REMOVE_USER_FROM_MAILING_GROUP, {'user_id': user_id, 'group_name': mailing_group.value})

    async def remove_user(self, user_id: int) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(DELETE_USER, {'user_id': user_id})

    async def update_user_role(self, user_id: int, new_role: ChatRole) -> None:
        async with self.engine.begin() as conn:
            await conn.execute(UPDATE_USER_ROLE, {'user_id': user_id, 'role_name': new_role.value})
