import uuid
from typing import Generic
from datetime import datetime

from fastapi_users import models
from fastapi_users.schemas import CreateUpdateDictModel


class UserRead(Generic[models.ID], CreateUpdateDictModel):
    id: int
    email: str
    username: str
    last_request: datetime
    last_login: datetime

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    username: str
    email: str
    password: str

from pydantic import BaseModel


class FooBar(BaseModel):
    count: int
    size: float = None