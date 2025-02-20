from enum import Enum


class ChatRole(Enum):
    ADMIN = 'admin'
    USER = 'user'
    DEVELOPER = 'developer'
    APPLICANT = 'applicant'

class NoticeAction(Enum):
    APPROVE = 'approve'
    DECLINE = 'decline'
    POSTPONE = 'postpone'
    BAN = 'ban'
