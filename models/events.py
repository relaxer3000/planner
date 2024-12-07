from pydantic import BaseModel
from beanie import Document


class Event(Document):

    class Settings:
        name = "events"

    creator: str | None = None
    title: str
    description: str
    tags: list[str] | None
    location: str | None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book Launch",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "tags": ["Book", "FastAPI"],
                "location": "Google Meet"
            }
        }
    }


class UpdateEvent(BaseModel):

    title: str | None = None
    description: str | None = None
    tags: list[str] | None
    location: str | None

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "FastAPI Book",
                "description": "We will be discussing the contents of the FastAPI book in this event.",
                "tags": ["Book", "FastAPI"],
                "location": "Google Meet"
            }
        }
    }
