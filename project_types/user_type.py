from typing import List, Dict
from datetime import datetime

from aiogram.types import User

from project_types.enum_types import ChatRole
from config_data import DATETIME_FORMAT


class UserType:
    def __init__(self, user: User | None = None,
                 is_subscribed: bool = True,
                 groups: List[str] | None = None,
                 role: ChatRole = ChatRole.APPLICANT,
                 last_update: datetime | None = None):
        if user is not None:
            self.id: int | None = user.id
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
        self.groups = groups if groups is not None else []
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

    def to_dict(self, all_groups: Dict[str, str]) -> dict:
        result = {'id': self.id,
                'username': self.username,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'is_subscribed': int(self.is_subscribed),
                'role': self.role.value,
                'last_update': self.last_update}
        for group in all_groups.keys():
            result[group] = int(group in self.groups)

        return result

    def represent_applicant(self) -> str:
        current_username = f'@{self.username}' if self.username else 'Не заданно'

        result = (f'ID пользователя: {self.id}\n'
                f'Username: {current_username}\n')
        if self.first_name:
            result += f'Имя: {self.first_name}\n'
        if self.last_name:
            result += f'Фамилия: {self.last_name}\n'
        result += f'Дата подачи заявки: {self.last_update.strftime(DATETIME_FORMAT)} CET (UTC+01:00).'
        return result


    def represent_user_full(self) -> str:
        groups_str = ', '.join(self.groups) or 'Нет'
        result = (f'ID пользователя: {self.id}\n'
                  f'Username: {self.username}\n')
        if self.first_name:
            result += f'Имя: {self.first_name}\n'
        if self.last_name:
            result += f'Фамилия: {self.last_name}\n'
        result += f'Текущая роль: {self.role.value}\n'
        result += f'Текущие группы: {groups_str}\n'
        result += f'Last update: {self.last_update.strftime(DATETIME_FORMAT)} CET (UTC+01:00).'

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
        groups = data.get('groups') or []
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
