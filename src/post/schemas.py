from dataclasses import dataclass
from datetime import datetime, date

from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str
    user_id: int


class LikePost(BaseModel):
    id: int


class PostAnalytics(BaseModel):
    date_from: date
    date_to: date


class PostRead(BaseModel):
    id: int
    text: str
    user_id: int
    likes: int
    created_at: str
    updated_at: str
    user_id: int


@dataclass
class Posts:
    date: date
    numbers: int
