# app/crud.py
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timezone
from .models import Event, Attendee

# app/crud.py
async def create_event(session: AsyncSession, *, event_in):
    event = Event(
        name=event_in.name,
        location=event_in.location,
        start_time=event_in.start_time,  
        end_time=event_in.end_time,
        max_capacity=event_in.max_capacity
    )
    session.add(event)
    await session.commit()        
    await session.refresh(event)  
    return event


async def list_upcoming_events(session: AsyncSession, limit: int = 20, offset: int = 0):
    now = datetime.now(timezone.utc)
    stmt = select(Event).where(Event.end_time > now).order_by(Event.start_time).limit(limit).offset(offset)
    res = await session.execute(stmt)
    return res.scalars().all()

async def get_event(session: AsyncSession, event_id):
    stmt = select(Event).where(Event.id == event_id).options(selectinload(Event.attendees))
    res = await session.execute(stmt)
    return res.scalar_one_or_none()

async def list_attendees(session: AsyncSession, event_id, limit: int = 100, offset: int = 0):
    stmt = select(Attendee).where(Attendee.event_id == event_id).order_by(Attendee.registered_at).limit(limit).offset(offset)
    res = await session.execute(stmt)
    return res.scalars().all()

async def register_attendee(session: AsyncSession, event_id, name, email):
    """
    This function:
    1) starts a transaction
    2) locks the event row FOR UPDATE (so concurrent registration attempts are serialized)
    3) checks duplicates and capacity
    4) inserts the attendee
    """
    from sqlalchemy import select
    from sqlalchemy.orm import with_loader_criteria

    # Use explicit transaction block to ensure atomicity
    async with session.begin():
        # lock the event row
        stmt = select(Event).where(Event.id == event_id).with_for_update()
        result = await session.execute(stmt)
        event = result.scalar_one_or_none()
        if not event:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

        now = datetime.now(timezone.utc)
        if event.end_time <= now:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Event has already ended")

        # check duplicate
        dup_stmt = select(Attendee).where(Attendee.event_id == event_id, Attendee.email == email)
        dup = (await session.execute(dup_stmt)).scalar_one_or_none()
        if dup:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered for this event")

        # count current attendees
        count_stmt = select(func.count()).select_from(Attendee).where(Attendee.event_id == event_id)
        count = (await session.execute(count_stmt)).scalar_one()
        if count >= event.max_capacity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Event is full")

        # create attendee
        attendee = Attendee(event_id=event_id, name=name, email=email)
        session.add(attendee)
        # flush so we can return the new attendee
        await session.flush()
        await session.refresh(attendee)
        return attendee
