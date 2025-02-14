from typing import List
from config_data import MESSAGE_MAX_LENGTH
from project_types.user_type import UserType

def split_message(text: str, max_length: int = MESSAGE_MAX_LENGTH) -> List[str]:
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]


def get_users_groups_text(users: List[UserType]) -> str:
    result = ""
    for user in users:
        groups_list = [group.value for group in user.groups]
        groups_string = ", ".join(groups_list)
        result += f'id: {user.id}, user: {user.full_name()}, groups: {groups_string}\n'
    result = result.strip()

    return result