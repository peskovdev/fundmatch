from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.main import Base


user_teams = Table(
    "user_teams",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)

    teams: Mapped[list[Team]] = relationship(secondary=user_teams, back_populates="members")

    team_managed: Mapped["Team"] = relationship(back_populates="manager")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    members: Mapped[list[User]] = relationship(secondary=user_teams, back_populates="teams")

    manager_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    manager: Mapped["User"] = relationship(back_populates="team_managed")
