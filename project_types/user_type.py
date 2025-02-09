from typing import List, Optional
from datetime import datetime

from aiogram.types import User

from project_types.enum_types import MailingGroup, ChatRole
from config_data import DATETIME_FORMAT


class UserType:
    def __init__(self, user: Optional[User] = None,
                 is_subscribed: bool = True,
                 groups: List[MailingGroup] | None = None,
                 role: ChatRole = ChatRole.APPLICANT,
                 last_update: datetime | None = None):
        if user is not None:
            self.id = user.id
            self.username = user.username if user.username else None
            self.first_name = user.first_name if user.first_name else None
            self.last_name = user.last_name if user.last_name else None
            self.is_bot = user.is_bot
        else:
            self.id = None
            self.username = None
            self.first_name = None
            self.last_name = None
            self.is_bot = False
        self.is_subscribed = is_subscribed
        self.groups = groups
        self.role = role
        self.last_update = last_update or datetime.now()

    def full_name(self) -> str:
        if self.username:
            return f'@{self.username}'
        if self.first_name:
            if self.last_name:
                return self.first_name + ' ' + self.last_name
            else:
                return self.first_name
        if self.last_name:
            return self.last_name
        return str(self.id)

    def to_dict(self) -> dict:
        return {'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_bot': self.is_bot,
                'is_subscribed': self.is_subscribed,
                'groups': self.groups,
                'role': self.role,
                'last_update': self.last_update}

    def represent_user(self) -> str:
        current_username = f'@{self.username}' if self.username else 'Не заданно'

        result = (f'ID пользователя: {self.id}\n'
                f'Username: {current_username}\n')
        if self.first_name:
            result += f'Имя: {self.first_name}\n'
        if self.last_name:
            result += f'Фамилия: {self.last_name}\n'
        result += f'Дата подачи заявки: {self.last_update.strftime(DATETIME_FORMAT)} CET (UTC+01:00).'
        return result

    def to_db_params(self) -> dict:
        return {
            'user_id': self.id,
            'user_name': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_bot': self.is_bot,
            'is_subscribed': self.is_subscribed,
            'role_name': self.role.value,
            'last_update': self.last_update,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'UserType':
        is_subscribed = bool(data.get('is_subscribed', True))
        groups = data.get('groups')
        role = data.get('role') or ChatRole(data.get('role_name')) or ChatRole.APPLICANT
        instance = cls(is_subscribed=is_subscribed, groups=groups, role=role)
        user_id = data.get('user_id') or data.get('id')
        if user_id is None:
            raise ValueError('Missing user_id')
        instance.id = user_id
        instance.username = data.get('username') or data.get('user_name')
        instance.first_name = data.get('first_name')
        instance.last_name = data.get('last_name')
        instance.is_bot = bool(data.get('is_bot', False))
        return instance
