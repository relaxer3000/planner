from pydantic import EmailStr, BaseModel
from beanie import Document, Link

from models.events import Event


class User(Document):

    class Settings:
        name = "users"

    email: EmailStr
    password: str
    username: str
    events: list[Link[Event]] | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "fastapi@packt.com",
                "password": "1111",
                "username": "fastapi",
            }
        }
    }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
