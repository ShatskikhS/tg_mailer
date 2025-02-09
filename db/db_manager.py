from datetime import datetime

from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from config_data import DATABASE_URL, DEFAULT_ROLE_NAME
from db.models import Base, ChatRoleTable, UserTable, MailingGroupTable, UserMailingGroupTable


class DatabaseManager:
    def __init__(self, db_url: str=DATABASE_URL):
        self.engine = create_async_engine(db_url)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def get_role_id_by_name(self, role_name: str):
        async with self.async_session() as session:
            result = await session.execute(select(ChatRoleTable.role_id).where(ChatRoleTable.role_name == role_name))
            return result.scalar()

    async def init_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def add_chat_role(self, role_name: str, role_description: str):
        async with self.async_session() as session:
            new_role = ChatRoleTable(role_name=role_name, role_description=role_description)
            session.add(new_role)
            await session.commit()

    async def delete_chat_role(self, role_id: int):
        async with self.async_session() as session:
            users_with_role = await session.execute(select(UserTable).where(UserTable.role_id == role_id))
            users_to_update = users_with_role.scalars().all()

            if users_to_update:
                default_role_id = await self.get_role_id_by_name(DEFAULT_ROLE_NAME)
                await session.execute(update(UserTable).where(UserTable.role_id == role_id).
                                      values(role_id=default_role_id))

            await session.execute(delete(ChatRoleTable).where(ChatRoleTable.role_id == role_id))
            await session.commit()

    async def add_mailing_group(self, group_name: str, group_description: str):
        async with self.async_session() as session:
            new_group = MailingGroupTable(group_name=group_name, group_description=group_description)
            session.add(new_group)
            await session.commit()

    async def add_user(self, user_id: int,
                       user_name: str,
                       first_name: str,
                       last_name: str,
                       is_bot: bool,
                       is_subscribed: bool,
                       role_id: int,
                       last_update: datetime):
        async with self.async_session() as session:
            new_user = UserTable(user_id=user_id,
                                 user_name=user_name,
                                 first_name=first_name,
                                 last_name=last_name,
                                 is_bot=is_bot,
                                 is_subscribed=is_subscribed,
                                 role_id=role_id,
                                 last_update=last_update)
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
                select(UserTable).join(ChatRoleTable).where(ChatRoleTable.role_name == role_name).
                options(selectinload(UserTable.role), selectinload(UserTable.mailing_groups)))
            return result.scalars().all()

    async def get_all_users(self):
        async with self.async_session() as session:
            result = await session.execute(select(UserTable).options(selectinload(UserTable.role),
                                                                     selectinload(UserTable.mailing_groups)))
            all_data = result.scalars().all()
            return all_data

    async def update_user_role(self, user_id: int, new_role_id: int):
        async with self.async_session() as session:
            user = await session.get(UserTable, user_id)
            if user:
                user.role_id = new_role_id
                await session.commit()

    async def add_user_to_mailing_group(self, user_id: int, group_id: int):
        async with self.async_session() as session:
            new_relation = UserMailingGroupTable(user_id=user_id, group_id=group_id)
            session.add(new_relation)
            await session.commit()

    async def remove_user_from_mailing_group(self, user_id: int, group_id: int):
        async with self.async_session() as session:
            await session.execute(
                delete(UserMailingGroupTable).
                where((UserMailingGroupTable.user_id == user_id) & (UserMailingGroupTable.group_id == group_id)))
            await session.commit()

    async def delete_mailing_group(self, group_id: int):
        async with self.async_session() as session:
            await session.execute(delete(UserMailingGroupTable).where(UserMailingGroupTable.group_id == group_id))
            await session.execute(delete(MailingGroupTable).where(MailingGroupTable.group_id == group_id))
            await session.commit()

# Для запуска инициализации базы данных
# import asyncio
# asyncio.run(init_db())
