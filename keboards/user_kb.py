from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from project_types.user_type import UserType


FEEDBACK_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад'), KeyboardButton(text='Отправить')]],
                                  resize_keyboard=True,
                                  one_time_keyboard=True,
                                  input_field_placeholder='Type your message here...')


def get_hone_usr_kb(user: UserType) -> ReplyKeyboardMarkup:
    """
    Returns a ReplyKeyboardMarkup object with keyboard options for specific user.
    :param user:
    :return:
    """
    if user.is_subscribed:
        sub_text = 'Отписаться от рассылки'
    else:
        sub_text = 'Подписаться на рассылку'
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=sub_text)],
                                         [KeyboardButton(text='Написать администраторам')],
                                         KeyboardButton(text='Справка')],
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Click button to continue')