from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.hash_password import HashPassword
from auth.jwt_handler import create_access_token
from models.users import User, TokenResponse
from database.objects import Database


user_router = APIRouter(tags=["User"])
user_database = Database(User)
hash_password = HashPassword()


@user_router.get('/', response_model=list[User])
async def get_all_users() -> list[User]:
    users = await user_database.get_all()
    return users


@user_router.get('/{user_id}')
async def get_user(user_id: PydanticObjectId) -> User:
    user = await user_database.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID doesn't exist",
        )
    return user


@user_router.post('/signup')
async def sign_user_up(user: User) -> dict:
    user_exists = await User.find_one(User.email == user.email)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with email provided exists already."
        )

    hashed_password = HashPassword.create_hash(user.password)
    user.password = hashed_password
    await user_database.create(user)
    return {"message": "User created successfully"}


@user_router.post("/signin", response_model=TokenResponse)
async def authenticate(user: OAuth2PasswordRequestForm = Depends()) -> dict:
    user_db = await User.find_one(User.email == user.username)
    if user_db is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Wrong password or username"
        )

    if hash_password.verify_hash(user.password, user_db.password):
        access_token = create_access_token(user_db.email)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong password or username"
    )


@user_router.delete('/{user_id}')
async def delete_user(user_id: PydanticObjectId) -> dict:
    user = await user_database.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with supplied ID doesn't exist",
        )

    await user_database.delete(user_id)
    return {"message": "User deleted successfully."}
