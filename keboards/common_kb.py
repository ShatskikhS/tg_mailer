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

BACK_HOME_TEXT_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад'), KeyboardButton(text='Домой')]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder="Type user's id here")

MAILING_START_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить всем'),
                                                  KeyboardButton(text='Выбрать группы для рассылки')],
                                                 [KeyboardButton(text='Домой')]],
                                       resize_keyboard=True,
                                       one_time_keyboard=True,
                                       input_field_placeholder='Click the button to continue')

GET_NEW_USER_INFO_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Не хочу представляться')]],
                                           resize_keyboard=True,
                                           one_time_keyboard=True,
                                           input_field_placeholder='Type your message here')

BACK_SEND_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад'), KeyboardButton(text='Отправить')]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True,
                                   input_field_placeholder='Click button to continue')

USER_GROUPS_HOME_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Все пользователи'),
                                                     KeyboardButton(text='Пользователи по группам')],
                                                    [KeyboardButton(text='Домой')]],
                                          resize_keyboard=True,
                                          one_time_keyboard=True,
                                          input_field_placeholder='Click button to continue')


def get_applicants_kb(back_button: bool = True, front_button: bool = True) -> ReplyKeyboardMarkup:
    nav_buttons = [KeyboardButton(text='Предыдущее'), KeyboardButton(text='Следующее')]
    if not back_button:
        nav_buttons.remove(KeyboardButton(text='Предыдущее'))
    if not front_button:
        nav_buttons.remove(KeyboardButton(text='Следующее'))

    kb = [[KeyboardButton(text='Отклонить'), KeyboardButton(text='Одобрить')]]
    if nav_buttons:
        kb.append(nav_buttons)
    kb.append([KeyboardButton(text='Домой')])
    return ReplyKeyboardMarkup(keyboard=kb,
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Click button to continue')
