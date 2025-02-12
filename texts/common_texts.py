from typing import List

from project_types.enum_types import MailingGroup


HOME = 'Вы находитесь в домашнем меню. Для продолжения нажмите кнопку.'

MAILING_START = 'Для отправки рассылки выберете опцию. Для возврата в домашнее меню нажмите "Домой"'

CHOSE_GROUPS = ('Выберите одну или несколько групп для рассылки и нажмите "голосовать" для продолжения.\n'
                'Для возврата в домашнее меню нажмите кнопку"Домой')

def get_input_text(groups: List[MailingGroup], nuber_users: int) -> str:
    group_text = ', '.join([group.value for group in groups])
    return (f'Сообщение будет отправлено группам: {group_text}\n'
            f'Всего будет отправлено {nuber_users} сообщений.\n'
            f'Для начала рассылки отправьте текст как сообщению боту.')


def mailing_result(mailed_number: int, mailing_fails: List[str]) -> str:
    fails_text = '\n'.join(mailing_fails)
    result_text = (f'Сообщение отправлено {mailed_number} пользователям.\n'
                   f'Ошибок отправки: {len(mailing_fails)}')

    if mailing_fails:
        result_text += f'\n{fails_text}'

    return result_text
