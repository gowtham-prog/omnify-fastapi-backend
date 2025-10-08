# app/models.py
import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from .db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    max_capacity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        CheckConstraint("max_capacity >= 0", name="ck_max_capacity_non_negative"),
    )

    attendees = relationship("Attendee", back_populates="event", cascade="all, delete-orphan")


class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(PG_UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    registered_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    event = relationship("Event", back_populates="attendees")

    __table_args__ = (
        UniqueConstraint("event_id", "email", name="uq_event_email"),
    )
