from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class ChatRole(Base):
    __tablename__ = "chat_role"

    role_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    role_description: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


class MailingGroup(Base):
    __tablename__ = "mailing_group"

    group_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    group_description: Mapped[str] = mapped_column(Text, unique=True, nullable=False)


class UserTable(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    is_bot: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    last_updated: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now())
    role_id: Mapped[int] = mapped_column(ForeignKey("chat_role.role_id"), nullable=False)
    role: Mapped[ChatRole] = relationship("ChatRole")
    mailing_groups: Mapped[List[MailingGroup]] = relationship(secondary="user_mailing_group", cascade="all, delete-orphan")


class UserMailingGroup(Base):
    __tablename__ = "user_mailing_group"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("mailing_group.group_id"), primary_key=True)


