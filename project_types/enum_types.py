from enum import Enum


class MailingGroup(Enum):
    GROUP1 = 'group1'
    GROUP2 = 'group2'
    GROUP3 = 'group3'


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