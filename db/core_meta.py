from sqlalchemy import MetaData, Table, Column, Integer, String, Boolean, DateTime, ForeignKey


metadata = MetaData()

chat_roles_table = Table(
    "chat_roles",
    metadata,
    Column('role_id', Integer, primary_key=True),
    Column('role_name', String, nullable=False, unique=True),
    Column('role_description', String)
)

mailing_groups_table = Table(
    'mailing_groups',
    metadata,
    Column('group_id', Integer, primary_key=True),
    Column('group_name', String, nullable=False, unique=True),
    Column('group_description', String)
)

users_table = Table(
    'users',
    metadata,
    Column('user_id', Integer, primary_key=True),
    Column('user_name', String, unique=True),
    Column('first_name', String),
    Column('last_name', String),
    Column('is_bot', Boolean, nullable=False),
    Column('is_subscribed', Boolean, nullable=False),
    Column('last_update', DateTime, nullable=False),
    Column('role_id', Integer, ForeignKey('chat_roles.role_id')),
)

users_mailing_groups_table = Table(
    'users_mailing_groups',
    metadata,
    Column('user_id', Integer, ForeignKey('users.user_id'), primary_key=True),
    Column('group_id', Integer, ForeignKey('mailing_groups.group_id'), primary_key=True),
)
