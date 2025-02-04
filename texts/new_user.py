from config import COMMUNITY_NAME
from project_types import UserType


NEW_USER_GREETINGS = (f'Вас приветствует бот новостной рассылки {COMMUNITY_NAME}!'
                      f'Для того чтобы подписаться на рассылку нажмите "Продолжить"')

APPLICATION_ACCEPTED = (f'Ваша заявка на подписку на рассылку сообщества {COMMUNITY_NAME}!'
                        f'передана администраторам. После того как заявка будет рассмотрена '
                        f'вы получите уведомление в этом чате.')

NEW_DEVELOPER = 'Вы были добавлены в бот как разработчик. Для перехода в домашнее меню нажмите "Домой"'


def new_app_notification(user: UserType):
    return (f'Поступила новая заявка на подписку на рассылку.\n'
            f'Данне заявителя:\n\n'
            f'{user.represent_user()}')