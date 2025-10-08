# app/schemas.py
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from uuid import UUID

IST = ZoneInfo("Asia/Kolkata")

class EventCreate(BaseModel):
    name: str
    location: Optional[str] = None
    start_time: datetime
    end_time: datetime
    max_capacity: int

    @validator("start_time", "end_time", pre=True)
    def ensure_tz(cls, value):
        # pydantic will parse str -> datetime
        if isinstance(value, str):
            dt = datetime.fromisoformat(value)
        else:
            dt = value
        if dt.tzinfo is None:
            # assume IST for naive datetimes
            dt = dt.replace(tzinfo=IST)
        # always convert to UTC for server
        return dt.astimezone(timezone.utc)

    @validator("max_capacity")
    def capacity_non_negative(cls, v):
        if v < 0:
            raise ValueError("max_capacity must be >= 0")
        return v

    @validator("end_time")
    def end_after_start(cls, v, values):
        start = values.get("start_time")
        if start and v <= start:
            raise ValueError("end_time must be after start_time")
        return v


class EventRead(BaseModel):
    id: UUID
    name: str
    location: Optional[str]
    start_time: datetime
    end_time: datetime
    max_capacity: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AttendeeCreate(BaseModel):
    name: str
    email: EmailStr


class AttendeeRead(BaseModel):
    id: UUID
    event_id: UUID
    name: str
    email: EmailStr
    registered_at: datetime

    class Config:
        orm_mode = True
