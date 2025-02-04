from typing import Dict, List

from config import BOT_ID, DEVELOPER_IDS
from db import DatabaseManager
from project_types import ChatRole, MailingGroup, UserType


class BotConfig:
    def __init__(self, db: DatabaseManager,
                 developer_ids: List[int] = DEVELOPER_IDS,
                 bot_id: int = BOT_ID):
        self.db = db
        self.users: Dict[int, UserType] | None = None
        self.bot_id: int = bot_id
        self.developer_ids: List[int] = developer_ids

    async def read_users(self) -> None:
        """
        This method reads the users from the database and updates self.users.
        This asynchronous method should always be run after the class instance is initialized.
        :return None:
        """
        # TODO: Complete method.
        pass

    async def add_user(self, user: UserType) -> None:
        """
        This method adds a new user to the database and updates self.users.
        :param user:
        :return None:
        """
        self.users[user.id] = user
        # TODO: save user to db.

    async def remove_user_by_id(self, user_id: int) -> None:
        """
        This method removes a user from the database and updates self.users.
        :param user_id:
        :return:
        """
        self.users.pop(user_id, None)
        # TODO: Remove user from db

    async def alter_user_role(self, user_id: int, new_role: ChatRole) -> None:
        """
        This method changes a user role in the database and updates self.users.
        :param user_id:
        :param new_role:
        :return:
        """
        self.users[user_id].role = new_role
        # TODO: add db method

    async def drop_users_group(self, user_id: int, group: MailingGroup) -> None:
        """
        Removes the user from the mailing group updates self.users and db.
        :param user_id:
        :param group:
        :return:
        """
        self.users[user_id].groups.remove(group)
        # TODO: add db method

    async def add_users_group(self, user_id: int, group: MailingGroup) -> None:
        if group in self.users[user_id].groups:
            self.users[user_id].groups.append(group)
        else:
            raise ValueError(f"User {self.users[user_id].full_name()} is already in hte mailing group {group.value}")
        # TODO: add db method

    async def change_subscriptions(self, user_id: int) -> bool:
        if self.users[user_id].is_subscribed:
            self.users[user_id].is_subscribed = False
            # TODO: Add db method
            return False
        else:
            self.users[user_id].is_subscribed = True
            # TODO: Add db method
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
