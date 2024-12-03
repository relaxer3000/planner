from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from models.users import User
from database.connection import get_session


user_router = APIRouter(tags=["User"])


@user_router.get('/')
async def get_all_users(session: Session = Depends(get_session)) -> Sequence[User]:
    users = session.exec(select(User)).all()
    return users


@user_router.get('/{user_id}')
async def get_user(user_id: int, session: Session = Depends(get_session)) -> User:
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID doesn't exist",
        )
    return user


@user_router.post('/')
async def create_user(user: User, session: Session = Depends(get_session)) -> User:
    user_db = User(**user.model_dump(exclude={'id'}))
    session.add(user_db)
    session.commit()
    session.refresh(user_db)
    return user_db


@user_router.delete('/{user_id}')
async def delete_user(user_id: int, session: Session = Depends(get_session)) -> dict:
    user = session.exec(select(User).where(User.id == user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID doesn't exist",
        )
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully."}
