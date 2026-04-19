from datetime import datetime

from sqlalchemy import String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String(128))
    headline: Mapped[str | None] = mapped_column(String(256))
    bio: Mapped[str | None] = mapped_column(Text)
    photo_file_id: Mapped[str | None] = mapped_column(String(256))
    cv_file_id: Mapped[str | None] = mapped_column(String(256))
    cv_file_name: Mapped[str | None] = mapped_column(String(256))
    locale: Mapped[str] = mapped_column(String(8), default="ru")
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now(), server_default=func.now()
    )


class Project(Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
    url: Mapped[str | None] = mapped_column(String(512))
    photo_file_id: Mapped[str | None] = mapped_column(String(256))
    position: Mapped[int] = mapped_column(default=0, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Experience(Base):
    __tablename__ = "experience"

    id: Mapped[int] = mapped_column(primary_key=True)
    company: Mapped[str] = mapped_column(String(128))
    role: Mapped[str] = mapped_column(String(128))
    period: Mapped[str] = mapped_column(String(64))
    description: Mapped[str | None] = mapped_column(Text)
    position: Mapped[int] = mapped_column(default=0, index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())


class Skill(Base):
    __tablename__ = "skill"
    __table_args__ = (UniqueConstraint("name", name="uq_skill_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64))
    category: Mapped[str | None] = mapped_column(String(64))
    position: Mapped[int] = mapped_column(default=0, index=True)


class Contact(Base):
    __tablename__ = "contact"
    __table_args__ = (UniqueConstraint("kind", name="uq_contact_kind"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(32))
    value: Mapped[str] = mapped_column(String(256))
    position: Mapped[int] = mapped_column(default=0, index=True)


class VisitorLog(Base):
    """Optional telemetry — who opened /start. Only tg_user_id, nothing sensitive."""

    __tablename__ = "visitor_log"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(index=True)
    tg_username: Mapped[str | None] = mapped_column(String(64))
    first_seen: Mapped[datetime] = mapped_column(server_default=func.now())
