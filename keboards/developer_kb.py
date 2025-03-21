from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from project_types.enum_types import ChatRole
from project_types.user_type import UserType

USER_MANAGEMENT_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Изменить роль'),
                                                    KeyboardButton(text='Изменить группу'),
                                                    KeyboardButton(text='Удалить пользователя')],
                                                   [KeyboardButton(text='Скачать xlsx таблицу')],
                                                   [KeyboardButton(text='Домой')]],
                                         resize_keyboard=True,
                                         input_field_placeholder='Click button to continue')

HOME_LIST_USERS_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='К списку пользователей')],
                                                   [KeyboardButton(text='Домой')]],
                                         resize_keyboard=True,
                                         one_time_keyboard=True,
                                         input_field_placeholder='Click button to continue')

MAILING_MANAGEMENT_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Удалить группу'),
                                                       KeyboardButton(text='Добавить группу')],
                                                      [KeyboardButton(text='Домой')]],
                                            resize_keyboard=True,
                                            one_time_keyboard=True,
                                            input_field_placeholder='Click button to continue'
                                            )


def get_mailing_management_kb(remove: bool = True) -> ReplyKeyboardMarkup:
    line1 = [KeyboardButton(text='Удалить группу'), KeyboardButton(text='Добавить группу')] if remove else [KeyboardButton(text='Добавить группу')]
    return ReplyKeyboardMarkup(keyboard=[line1,
                                         [KeyboardButton(text='Домой')]],
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Click button to continue'
                               )


def home_developer_kb(user:UserType) -> ReplyKeyboardMarkup:
    if user.is_subscribed:
        sub_text = 'Отписаться от рассылки'
    else:
        sub_text = 'Подписаться на рассылку'

    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=sub_text)],
                                         [KeyboardButton(text='Рассылка')],
                                         [KeyboardButton(text='Запросы'),
                                          KeyboardButton(text='Пользователи'),
                                          KeyboardButton(text='Группы')]],
                               resize_keyboard=True,
                               input_field_placeholder='Click button to continue')


def update_roles_kb(user: UserType) -> ReplyKeyboardMarkup:
    line1 = [KeyboardButton(text=role.value) for role in ChatRole if role not in (user.role, ChatRole.APPLICANT)]
    return ReplyKeyboardMarkup(keyboard=[line1,
                                         [KeyboardButton(text='Назад')],
                                         [KeyboardButton(text='Домой')]],
                               resize_keyboard=True,
                               input_field_placeholder='Click button to continue')
