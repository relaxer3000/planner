from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database.connection import get_session
from models.events import Event, UpdateEvent
from models.users import User

event_router = APIRouter(tags=["Event"])


@event_router.get('/')
async def get_events(session: Session = Depends(get_session)) -> Sequence[Event]:
    events = session.exec(select(Event)).all()
    return events


@event_router.get('/{event_id}')
async def get_event(event_id: int, session: Session = Depends(get_session)) -> Event:
    event = session.exec(select(Event).where(Event.id == event_id)).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID doesn't exist"
        )
    return event


@event_router.post('/')
async def create_event(event: Event, session: Session = Depends(get_session)) -> Event:
    user = session.exec(select(User).where(User.id == Event.user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with user_id not found"
        )

    event_db = Event(**event.model_dump(exclude={'id'}))
    session.add(event_db)
    session.commit()
    session.refresh(event_db)

    return event_db


@event_router.patch('/{event_id}')
async def update_event(event_id: int, event: UpdateEvent, session: Session = Depends(get_session)) -> Event:
    event_db = session.exec(select(Event).where(Event.id == event_id)).first()
    if event_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID not found"
        )
    for k, v in event.model_dump(exclude={'user_id'}).items():
        if v is not None:
            setattr(event_db, k, v)

    if event.user_id:
        user = session.exec(select(User).where(User.id == Event.user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with id = Event.user_id not found"
            )
        event_db.user = user

    session.add(event_db)
    session.commit()
    session.refresh(event_db)

    return event_db


@event_router.delete('/{event_id}')
async def delete_event(event_id: int, session: Session = Depends(get_session)) -> dict:
    event = session.exec(select(Event).where(Event.id == event_id)).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID not found"
        )

    session.delete(event)
    session.commit()

    return {"message": "event was deleted"}
