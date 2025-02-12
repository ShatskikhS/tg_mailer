from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


PROCEED_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Продолжить')]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True,
                                 input_field_placeholder='Click the button to continue')

HOME_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Домой')]],
                              resize_keyboard=True,
                              input_field_placeholder='Click the button to continue')

BACK_HOME_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад'), KeyboardButton(text='Домой')]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='Click the button to continue')

MAILING_START_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить всем'),
                                                  KeyboardButton(text='Выбрать группы для рассылки')],
                                                 [KeyboardButton(text='Домой')]],
                                       resize_keyboard=True,
                                       one_time_keyboard=True,
                                       input_field_placeholder='Click the button to continue')

BACK_HOME = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад')],
                                               [KeyboardButton(text='Домой')]],
                                resize_keyboard=True,
                                one_time_keyboard=True,
                                input_field_placeholder='Type your message here')
