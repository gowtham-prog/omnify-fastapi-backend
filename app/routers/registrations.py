# app/routers/registrations.py
from fastapi import APIRouter, Depends, status, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import AttendeeCreate, AttendeeRead
from ..db import get_session
from .. import crud

router = APIRouter()

@router.post("/events/{event_id}/register", response_model=AttendeeRead, status_code=status.HTTP_201_CREATED)
async def register_attendee(event_id: str, payload: AttendeeCreate, session: AsyncSession = Depends(get_session)):
    attendee = await crud.register_attendee(session, event_id, payload.name, payload.email)
    return attendee

@router.get("/events/{event_id}/attendees", response_model=list[AttendeeRead])
async def get_attendees(event_id: str, limit: int = Query(100, ge=1), offset: int = Query(0, ge=0),
                        session: AsyncSession = Depends(get_session)):
    return await crud.list_attendees(session, event_id, limit=limit, offset=offset)
