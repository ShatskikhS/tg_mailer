from datetime import datetime
from typing import List

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config import DATABASE_URL, DEFAULT_ROLE
from db.models import Base, ChatRole, UserTable, MailingGroup, UserMailingGroup
from project_types import UserType


class DatabaseManager:
    def __init__(self, db_url: str=DATABASE_URL):
        self.engine = create_async_engine(db_url)
        self.async_session = async_sessionmaker(self.engine.engine, expire_on_commit=False)

    async def get_role_id_by_name(self, role_name: str):
        async with self.async_session() as session:
            result = await session.execute(select(ChatRole.role_id).where(ChatRole.role_name == role_name))
            return result.scalar()

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_chat_role(self, role_name: str, role_description: str):
        async with self.async_session() as session:
            new_role = ChatRole(role_name=role_name, role_description=role_description)
            session.add(new_role)
            await session.commit()

    async def delete_chat_role(self, role_id: int):
        async with self.async_session() as session:
            users_with_role = await session.execute(select(UserTable).where(UserTable.role_id == role_id))
            users_to_update = users_with_role.scalars().all()

            if users_to_update:
                default_role_id = await self.get_role_id_by_name(DEFAULT_ROLE.value)
                await session.execute(update(UserTable).where(UserTable.role_id == role_id).
                                      values(role_id=default_role_id))

            await session.execute(delete(ChatRole).where(ChatRole.role_id == role_id))
            await session.commit()

    async def add_mailing_group(self, group_name: str, group_description: str):
        async with self.async_session() as session:
            new_group = MailingGroup(group_name=group_name, group_description=group_description)
            session.add(new_group)
            await session.commit()

    async def add_user(self, user: UserType):
        async with self.async_session() as session:
            role_id = await self.get_role_id_by_name(user.role.value)
            new_user = UserTable(user_id=user.id,
                                 user_name=user.username ,
                                 first_name=user.first_name,
                                 last_name=user.last_name,
                                 is_bot=user.is_bot,
                                 is_subscribed=user.is_subscribed,
                                 role_id=role_id,
                                 last_updated=datetime.now())
            session.add(new_user)
            await session.commit()

    async def delete_user(self, user_id: int):
        async with self.async_session() as session:
            await session.execute(delete(UserTable).where(UserTable.user_id == user_id))
            await session.commit()

    async def get_user(self, user_id: int):
        async with self.async_session() as session:
            result = await session.execute(
                select(UserTable).where(UserTable.user_id == user_id).
                options(selectinload(UserTable.role), selectinload(UserTable.mailing_groups)))
            return result.scalars().first()

    async def get_users_by_role(self, role_name: str):
        async with self.async_session() as session:
            result = await session.execute(
                select(UserTable).join(ChatRole).where(ChatRole.role_name == role_name).
                options(selectinload(UserTable.role), selectinload(UserTable.mailing_groups)))
            return result.scalars().all()

    async def get_all_users(self) -> List[UserType]:
        async with self.async_session() as session:
            result = await session.execute(select(UserTable).options(selectinload(UserTable.role),
                                                                     selectinload(UserTable.mailing_groups)))
            all_data = result.scalars().all()
            return result.scalars().all()

    async def update_user_role(self, user_id: int, new_role_id: int):
        async with self.async_session() as session:
            user = await session.get(UserTable, user_id)
            if user:
                user.role_id = new_role_id
                await session.commit()

    async def add_user_to_mailing_group(self, user_id: int, group_id: int):
        async with self.async_session() as session:
            new_relation = UserMailingGroup(user_id=user_id, group_id=group_id)
            session.add(new_relation)
            await session.commit()

    async def remove_user_from_mailing_group(self, user_id: int, group_id: int):
        async with self.async_session() as session:
            await session.execute(
                delete(UserMailingGroup).
                where((UserMailingGroup.user_id == user_id) & (UserMailingGroup.group_id == group_id)))
            await session.commit()

    async def delete_mailing_group(self, group_id: int):
        async with self.async_session() as session:
            await session.execute(delete(UserMailingGroup).where(UserMailingGroup.group_id == group_id))
            await session.execute(delete(MailingGroup).where(MailingGroup.group_id == group_id))
            await session.commit()

# Для запуска инициализации базы данных
# import asyncio
# asyncio.run(init_db())
