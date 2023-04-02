from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str
    user_id: int


class LikePost(BaseModel):
    id: int


class PostRead(BaseModel):
    id: int
    text: str
    user_id: int
    likes: int
    created_at: str
    updated_at: str
    user_id: int
