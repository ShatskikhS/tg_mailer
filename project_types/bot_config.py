from typing import Dict, List

from config_data import BOT_ID, DEVELOPER_IDS
from db.raw_sql import RawSQL
from project_types.enum_types import ChatRole, MailingGroup
from project_types.user_type import UserType


class BotConfig:
    def __init__(self, db_manager: RawSQL,
                 developer_ids: List[int] = DEVELOPER_IDS,
                 bot_id: int = BOT_ID):
        self.db_manager = db_manager
        self.users: Dict[int, UserType] | None = None
        self.bot_id: int = bot_id
        self.developer_ids: List[int] = developer_ids

    async def init_config(self):
        await self.db_manager.init_db()
        self.users = await self.db_manager.get_all_users()

    async def add_user(self, user: UserType) -> None:
        """
        This method adds a new user to the database and updates self.users.
        :param user:
        :return None:
        """
        self.users[user.id] = user
        await self.db_manager.add_user(user)
        for group in user.groups:
            await self.db_manager.add_user_to_mailing_group(user_id=user.id,mailing_group=group)

    async def remove_user_by_id(self, user_id: int) -> None:
        """
        This method removes a user from the database and updates self.users.
        :param user_id:
        :return:
        """
        if user_id not in self.users.keys():
            raise ValueError('User_id not found')
        current_user = self.users.get(user_id)
        for group in current_user.groups:
            await self.db_manager.remove_user_from_mailing_group(user_id=user_id,mailing_group=group)
        await self.db_manager.remove_user(user_id=user_id)
        self.users.pop(user_id)

    async def alter_user_role(self, user_id: int, new_role: ChatRole) -> None:
        """
        This method changes a user role in the database and updates self.users.
        :param user_id:
        :param new_role:
        :return:
        """
        self.users[user_id].role = new_role
        await self.db_manager.update_user_role(user_id=user_id, new_role=new_role)

    async def drop_user_mailing_group(self, user_id: int, group: MailingGroup) -> None:
        """
        Removes the user from the mailing group updates self.users and db.
        :param user_id:
        :param group:
        :return:
        """
        self.users[user_id].groups.remove(group)
        await self.db_manager.remove_user_from_mailing_group(user_id=user_id,mailing_group=group)

    async def add_user_to_mailing_group(self, user_id: int, group: MailingGroup) -> None:
        if group in self.users[user_id].groups:
            self.users[user_id].groups.append(group)
        else:
            raise ValueError(f"User {self.users[user_id].full_name()} is already in hte mailing group {group.value}")
        await self.db_manager.add_user_to_mailing_group(user_id=user_id,mailing_group=group)

    async def change_subscriptions(self, user_id: int) -> bool:
        if self.users[user_id].is_subscribed:
            self.users[user_id].is_subscribed = False
            await self.db_manager.update_user_subscription(user_id=user_id, is_subscribed=False)
            return False
        else:
            self.users[user_id].is_subscribed = True
            await self.db_manager.update_user_subscription(user_id=user_id, is_subscribed=True)
            return True

    def get_ids_by_role(self, role: ChatRole) -> List[int]:
        result = []
        for user in self.users.values():
            if user.role == role:
                result.append(user.id)
        return result

    def get_role_by_id(self, user_id: int) -> ChatRole:
        return self.users[user_id].role

    def ger_user_by_id(self, user_id: int) -> UserType:
        return self.users[user_id]
