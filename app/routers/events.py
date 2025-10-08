# app/routers/events.py
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import EventCreate, EventRead
from ..db import get_session
from .. import crud

router = APIRouter()

@router.post("/events", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(payload: EventCreate, session: AsyncSession = Depends(get_session)):
    event = await crud.create_event(session, event_in=payload)
    return event

@router.get("/events", response_model=list[EventRead])
async def list_events(
    upcoming: bool = Query(True),
    limit: int = Query(20, ge=0, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session)
):
    if upcoming:
        return await crud.list_upcoming_events(session, limit=limit, offset=offset)
    return await crud.list_all_events(session, limit=limit, offset=offset)

@router.get("/events/{event_id}", response_model=EventRead)
async def get_event(event_id: str, session: AsyncSession = Depends(get_session)):
    return await crud.get_event(session, event_id)