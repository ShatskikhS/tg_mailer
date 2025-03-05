from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from project_types.user_type import UserType


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
                                   input_field_placeholder="Type here...")


Y_N_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Нет'), KeyboardButton(text='Да')]],
                             resize_keyboard=True,
                             one_time_keyboard=True,
                             input_field_placeholder='Click the button to continue'
                             )

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
                                                     KeyboardButton(text='Пользователи без группы')],
                                                    [KeyboardButton(text='Пользователи группы'),
                                                     KeyboardButton(text='Пользователи не в группе')],
                                                    [KeyboardButton(text='Домой')]],
                                          resize_keyboard=True,
                                          one_time_keyboard=True,
                                          input_field_placeholder='Click button to continue')

CONTINUE_BACK_HOME_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Назад'), KeyboardButton(text='Продолжить')],
                                                      [KeyboardButton(text='Домой')]],
                                            resize_keyboard=True,
                                            one_time_keyboard=True,
                                            input_field_placeholder='Click button to continue'
                                            )

ADD_TO_GROUP_HOME_KB = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Добавить в группу')],
                                                     [KeyboardButton(text='Домой')]],
                                           resize_keyboard=True,
                                           one_time_keyboard=True,
                                           input_field_placeholder='Click button to continue'
                                           )

EDIT_GROUPS_HOME = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Редактировать группы пользователя')],
                                                 [KeyboardButton(text='Домой')]],
                                       resize_keyboard=True,
                                       one_time_keyboard=True,
                                       input_field_placeholder='Click button to continue'
                                       )


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

def groups_home_kb(btn_names:List[str]) -> ReplyKeyboardMarkup:
    line1 = [KeyboardButton(text=name) for name in btn_names]
    return ReplyKeyboardMarkup(keyboard=[line1,
                                         [KeyboardButton(text='Назад')],
                                         [KeyboardButton(text='Домой')]],
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Click button to continue')


def edit_groups_kb(user: UserType, all_groups: List[str], back: bool = True) -> ReplyKeyboardMarkup:
    line1 = [KeyboardButton(text=f'Добавить в {group}') for group in all_groups if group not in user.groups]
    line2 = [KeyboardButton(text=f'Удалить из {group}') for group in user.groups]
    kb = [line1, line2]
    if back:
        kb.append([KeyboardButton(text='Назад')])
    kb.append([KeyboardButton(text='Домой')])
    return ReplyKeyboardMarkup(keyboard=kb,
                               resize_keyboard=True,
                               one_time_keyboard=True,
                               input_field_placeholder='Click button to continue'
                               )
