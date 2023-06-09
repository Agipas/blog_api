from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from database import Base


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("user.id"))


class PostLogs(Base):
    __tablename__ = "post_logs"
    id = Column(Integer, primary_key=True, index=True)
    dislikes = Column(Boolean, nullable=True)
    likes = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey("post.id"))

