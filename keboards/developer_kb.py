from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from project_types.user_type import UserType


def get_home_developer_kb(user:UserType) -> ReplyKeyboardMarkup:
    if user.is_subscribed:
        sub_text = 'Отписаться от рассылки'
    else:
        sub_text = 'Подписаться на рассылку'

    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=sub_text)],
                                         [KeyboardButton(text='Рассылка')],
                                         [KeyboardButton(text='Запросы на вступление'),
                                          KeyboardButton(text='Управление пользовательскими группами')],
                                         [KeyboardButton(text='Управление пользователями'), KeyboardButton(text='Управление группами рассылок')]],
                               resize_keyboard=True,
                               input_field_placeholder='Click button to continue')