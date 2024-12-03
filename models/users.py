from pydantic import EmailStr
from sqlmodel import SQLModel, Field as SQLField, Relationship


class User(SQLModel, table=True):
    id: int | None = SQLField(default=None, nullable=False, primary_key=True)
    email: EmailStr
    username: str
    events: list['Event'] = Relationship(back_populates="user")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "fastapi@packt.com",
                "username": "fastapi",
            }
        }
    }
