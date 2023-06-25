from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.enums import EventStatus
from app.db.main import Base


user_teams = Table(
    "user_teams",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("team_id", ForeignKey("teams.id", ondelete="CASCADE"), primary_key=True),
)


participant_events = Table(
    "participant_events",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column("event_id", ForeignKey("events.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    phone: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)

    teams: Mapped[list[Team]] = relationship(secondary=user_teams, back_populates="members")
    events: Mapped[list[Event]] = relationship(
        secondary=participant_events, back_populates="participants"
    )

    team_managed: Mapped["Team"] = relationship(back_populates="manager")


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))

    members: Mapped[list[User]] = relationship(secondary=user_teams, back_populates="teams")

    manager_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    manager: Mapped["User"] = relationship(back_populates="team_managed")

    events: Mapped[list[Event]] = relationship("Event", back_populates="team")

    @property
    def count_members(self):
        return len(self.members)

    @property
    def count_events(self):
        return len(self.events)


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey("teams.id", ondelete="CASCADE"))
    team: Mapped[Team] = relationship("Team", back_populates="events")
    participants: Mapped[list[User]] = relationship(
        "User", secondary=participant_events, back_populates="events"
    )
    contributions: Mapped[list[Contribution]] = relationship("Contribution", back_populates="event")
    goal: Mapped[float] = mapped_column(Float)
    current_amount: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255), nullable=True)
    event_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)

    def __init__(
        self, title: str, team: Team, goal: float, address: str, event_time: str, notes: str
    ):
        self.title = title
        self.goal = goal
        self.team = team
        self.team_id = team.id
        self.participants = team.members
        self.current_amount = 0.0
        self.status = EventStatus.MONEY_COLLECTING
        self.address = address
        self.event_time = self.parse_event_time(event_time)
        self.notes = notes

    def _update_current_amount(self):
        self.current_amount = sum(contribution.amount for contribution in self.contributions)

    def make_payment(self, user: User) -> None:
        amount = self.goal/len(self.participants)
        contribution = Contribution(user=user, event=self, amount=amount)
        self.contributions.append(contribution)
        self._update_current_amount()

    @staticmethod
    def parse_event_time(event_time: str) -> datetime:
        # Парсинг времени проведения в формате DD.MM.YYYY HH:MM
        datetime_format = "%d/%m/%Y"
        parsed_time = datetime.strptime(event_time, datetime_format)
        return parsed_time


class Contribution(Base):
    __tablename__ = "contributions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id", ondelete="SET NULL"))
    amount: Mapped[float] = mapped_column(Float)

    user: Mapped[User] = relationship("User")
    event: Mapped[Event] = relationship("Event", back_populates="contributions")
