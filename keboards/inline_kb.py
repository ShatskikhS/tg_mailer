from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData

from project_types.enum_types import NoticeAction


class NewUserNotice(CallbackData, prefix='new_app'):
    user_id: int
    action: NoticeAction


def get_new_app_notice_kb(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Отклонить', callback_data=NewUserNotice(user_id=user_id, action=NoticeAction.DECLINE).pack()),
                                                  InlineKeyboardButton(text='Принять', callback_data=NewUserNotice(user_id=user_id, action=NoticeAction.APPROVE).pack())],
                                                 [InlineKeyboardButton(text='Отложить', callback_data=NewUserNotice(user_id=user_id, action=NoticeAction.POSTPONE).pack())]])
