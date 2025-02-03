from aiogram.types import ReplyKeyboardMarkup , KeyboardButton


PROCEED_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Продолжить')]],
                                 resize_keyboard=True,
                                 one_time_keyboard=True,
                                 input_field_placeholder='Click the button to continue')

