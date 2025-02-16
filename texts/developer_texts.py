from typing import List

from project_types.user_type import UserType


CHOSE_ACTION = 'Выберете действие'

CHOSE_NEW_ROLE = 'Выберите новую роль для пользователя'

ROLE_HAS_UPDATED = 'Роль пользователя обновлена. Для возврата в домашнее меню нажмите "Домой"'


def users_list_text(users: List[UserType]) -> str:
    return '\n'.join([f'ID: {user.id}, username: {user.full_name()}, role: {user.role.value}' for user in users])
