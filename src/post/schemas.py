from datetime import date
from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str
    user_id: int
