from config_data import COMMUNITY_NAME
from project_types.user_type import UserType


NEW_USER_GREETINGS = (f'Вас приветствует бот новостной рассылки {COMMUNITY_NAME}!'
                      f'Для того чтобы подписаться на рассылку нажмите "Продолжить"')

APPLICATION_ACCEPTED = (f'Ваша заявка на подписку на рассылку сообщества {COMMUNITY_NAME}!'
                        f'передана администраторам. После того как заявка будет рассмотрена '
                        f'вы получите уведомление в этом чате.')

NEW_DEVELOPER = 'Вы были добавлены в бот как разработчик. Для перехода в домашнее меню нажмите "Домой"'

GET_USER_INFO_TEXT = ('Для упрощения работы администраторов представьтесь. Отправьте пару слов о себе как обычное сообщение этому боту.\n'
                      'Если Вас и хорошо знают и нет смысла в представлении или если вы просто не хотите представляться, Нажмите кнопку "Не хочу представляться"')

CONFIRM_INFO_TEXT = ('Для отправки заявки нажмите "Отправить".\n'
                     'Для того чтобы изменить предоставленную информацию, нажмите "Назад"')

APPLICANT_APPROVED = ('Ваша заявка одобрена!\n'
                      'Для перехода в домашнее меню нажмите "Домой"')

APPLICANT_DECLINED = 'Ваша заявка отклонена'


def new_app_notification(user: UserType, user_info: str) -> str:
    return (f'В бот поступила новая заявка\n'
            f'Данне заявителя:\n'
            f'{user.represent_user()}\n'
            f'Предоставленная информация о себе:\n'
            f'{user_info}')


def current_app_notification(user: UserType, user_info: str, user_number: int, total: int) -> str:
    return (f'Заявка №{user_number}/{total}.\n'
            f'Данные заявителя:\n'
            f'{user.represent_user()}\n'
            f'Предоставленная информация о себе:\n'
            f'{user_info}\n')
