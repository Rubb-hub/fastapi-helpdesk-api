from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


# new version of the Incident model using SQLAlchemy 2.0 style
class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    inc_title: Mapped[str] = mapped_column(String)
    inc_description: Mapped[str | None] = mapped_column(String, nullable=True)
    inc_state: Mapped[str] = mapped_column(String)
    inc_priority: Mapped[str] = mapped_column(String)
    inc_assignee: Mapped[str] = mapped_column(String)
    inc_create_date: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    user_login: Mapped[str] = mapped_column(String(10), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, server_default="user")  # Default role is "user". This value is given by the database if no role is provided when creating a new user. The role can be "user" or "admin".
