from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends

from auth.authenticate import authenticate
from database.objects import Database
from models.events import Event, UpdateEvent

event_router = APIRouter(tags=["Event"])
event_database = Database(Event)


@event_router.get('/')
async def get_events() -> list[Event]:
    events = await event_database.get_all()
    return events


@event_router.get('/{event_id}')
async def get_event(event_id: PydanticObjectId) -> Event:
    event = await event_database.get(event_id)
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID doesn't exist"
        )
    return event


@event_router.post('/')
async def create_event(body: Event, user: str = Depends(authenticate)) -> dict:
    body.creator = user
    await event_database.create(body)
    return {"message": "Event created successfully"}


@event_router.patch('/{event_id}')
async def update_event(
        event_id: PydanticObjectId,
        body: UpdateEvent,
        user: str = Depends(authenticate)) -> Event:

    event = await event_database.get(event_id)

    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed"
        )

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with user_id not found"
        )

    return_event = await event_database.update(event_id, body)
    return return_event


@event_router.delete('/{event_id}')
async def delete_event(event_id: PydanticObjectId, user: str = Depends(authenticate)) -> dict:
    event = await event_database.get(event_id)

    if event.creator != user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed"
        )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID not found"
        )

    await event_database.delete(event_id)
    return {"message": "event was deleted"}
