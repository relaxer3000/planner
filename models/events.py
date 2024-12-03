from pydantic import BaseModel
from sqlmodel import SQLModel, Field as SQLField, Relationship

from models.users import User


class Event(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    title: str
    description: str
    user_id: int | None = SQLField(default=None, foreign_key="user.id")
    user: User | None = Relationship(back_populates="events")

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "user_id": 1
            }
        }
    }


class UpdateEvent(BaseModel):
    title: str | None = None
    description: str | None = None
    user_id: int | None = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "user_id": 2
            }
        }
    }
