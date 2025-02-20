from typing import List

from project_types.user_type import UserType
from project_types.bot_config import BotConfig


CHOSE_ACTION = 'Выберете действие'

CHOSE_NEW_ROLE = 'Выберите новую роль для пользователя'

ROLE_HAS_UPDATED = 'Роль пользователя обновлена. Для возврата в домашнее меню нажмите "Домой"'

INPUT_GROUP_NAME = ('Отправьте имя новой группы боту как обычное сообщение.\n'
                    'Для возврата воспользуйтесь кнопками.')


def users_list_text(users: List[UserType]) -> str:
    return '\n'.join([f'ID: {user.id}, username: {user.full_name()}, role: {user.role.value}' for user in users])


def mailing_management_text(config: BotConfig) -> str:
    result = 'Группы для рассылок:\n'
    result += '\n'.join([f'{name}: {description} - {len(config.get_ids_by_mailing_group(name))} участников' for name, description in config.all_groups.items()])
    result += '\n\nДля продолжения нажмите кнопку'
    return result


def input_group_description_text(group_name: str) -> str:
    return (f'Имя новой группы: {group_name}\n'
            f'Для продолжения отправьте сообщение с описанием группы.')


def confirm_new_group_data(name: str, description: str) -> str:
    return (f'Название новой группы: {name}\n'
            f'Описание: {description}\n'
            f'Для продолжения нажмите "Продолжить", для возврата воспользуйтесь соответствующей кнопкой')


def confirm_group_delete_text(group_name: str, users_number: int) -> str:
    result =  (f'Название группы: {group_name}\n'
               f'Количество участников группы: {users_number}\n')
    if users_number != 0:
        result += 'Эта группа будет обнулена для всех действующих участников\n'
    result += f'Подтверждаете удаление?'
    return result
