from typing import List

from project_types.bot_config import BotConfig

HOME = 'Вы находитесь в домашнем меню. Для продолжения нажмите кнопку.'

MAILING_START = 'Для отправки рассылки выберете опцию. Для возврата в домашнее меню нажмите "Домой"'

CHOSE_GROUPS = ('Выберите одну или несколько групп для рассылки и нажмите "голосовать" для продолжения.\n'
                'Для возврата в домашнее меню нажмите кнопку"Домой')

APPLICANT_NOTICE_APPROVED = 'Заявка одобрена. Пользователь подписан на рассылку. Добавить его в группы рассылок Вы можете в домашнем меню.'

APPLICANT_NOTICE_DECLINED = 'Заявка отклонена. Пользователь удален из бота.'

APPLICANT_NOTICE_POSTPONED = 'Решение отложено. Одобрить или отклонить заявку вы можете в домашнем меню бота.'

USER_GROUPS_HOME_TEXT = ('В этом разделе можно добавить пользователей в группы рассылок или удалить пользователей из этих групп.\n'
                         '"Все пользователи" - показать всех пользователей и их группы\n'
                         '"Пользователи группы" - показать пользователей одной группы по выбору. Может быть удобным, если Вам нужно удалить пользователя из группы для рассылки\n'
                         '"Пользователи не в группе" - показать пользователей не состоящих в группе. Может быть удобным, если Вам нужно добавить пользователя в эту группу.')

CHOSE_USER_TEXT = ('Для редактирования пользователя из списка отправьте его id как сообщение боту.\n'
                   'Для возврата в предыдущее меню нажмите "Назад".\n'
                   'Для возврата в домашнее меню нажмите "Домой".')

ID_IS_TEXT = 'Ошибка: Неверно введен ID пользователя. ID может состоять только из цифр.'

ID_NOT_IN_LIST = 'Ошибка: Неверно введен ID пользователя. ID пользователя должен присутствовать в списке'

NEW_APPLICANT_APPROVED = 'Заявитель одобрен. Нажмите "Добавить в группу" для добавления пользователя в группу рассылки или "Домой" для возврата в домашнее меню.'

def get_input_text(groups: List[str], nuber_users: int) -> str:
    group_text = ', '.join(groups)
    return (f'Сообщение будет отправлено группам: {group_text}\n'
            f'Всего будет отправлено {nuber_users} сообщений.\n'
            f'Для начала рассылки отправьте текст как сообщению боту.')


def mailing_result(mailed_number: int, mailing_fails: List[str]) -> str:
    fails_text = '\n'.join(mailing_fails)
    result_text = (f'Сообщение отправлено {mailed_number} пользователям.\n'
                   f'Ошибок отправки: {len(mailing_fails)}')

    if len(mailing_fails) > 0:
        result_text += f'\n{fails_text}'

    return result_text


def applicant_declined_text(amin_name: str, date: str) -> str:
    return f'Данная заявка была отклонена администратором {amin_name}, {date} CET'


def applicant_approved_text(amin_name: str, date: str) -> str:
    return f'Данная заявка была одобрена администратором {amin_name}, {date} CET'

def chose_groups_text(config: BotConfig, chosen_groups: List[str]) -> str:
    if chosen_groups:
        result = 'Выбранные группы:\n'
    else:
        result = 'Нет выбранных групп.\n'
    for group in chosen_groups:
        result += f'{group}: {config.all_groups.get(group) or ""}\n'
    result += (f'Текущее число получателей {len(config.get_mailing_ids(chosen_groups))}.\n'
               f'Для выбора групп воспользуйтесь кнопками.\n')
    if chosen_groups:
        result += 'Для просмотра потенциальных получателей сообщения нажмите "Получатели"\n'
    return result


def show_recipients_text(groups: List[str], config: BotConfig) -> str:
    result = 'Получатели сообщения:\n\n'
    ids = config.get_mailing_ids(groups)
    if not ids:
        return 'Получателей не найдено!'
    for current_id in ids:
        result += f'{config.users[current_id].full_name()}\n'
    return result
