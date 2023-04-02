from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
# from database import Base
from sqlalchemy.ext.declarative import declarative_base
metadata = MetaData()

Base = declarative_base(metadata=metadata)

# post = Table(
#     "post",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("text", String, nullable=False),
#     Column("likes", Integer, default=0),
#     # Column("dislike", Integer, default=0),
#     Column("created_at", TIMESTAMP, default=datetime.utcnow),
#     Column("updated_at", TIMESTAMP, default=datetime.utcnow),
#     Column("user_id", Integer, ForeignKey("user.id"), nullable=False)
# )


# post_logs = Table(
#     "post_logs",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("like", Boolean, nullable=True),
#     Column("dislike", Boolean, nullable=True),
#     Column("created_at", TIMESTAMP, default=datetime.utcnow),
#     Column("post_id", Integer, ForeignKey("post.id"), nullable=False)
# )

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    likes = Column(Integer, default=0)
    # dislikes = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    def __init__(self, metadata):
        self.__table__ = metadata.tables[self.__tablename__]


class PostLogs(Base):
    __tablename__ = "post_logs"
    id = Column(Integer, primary_key=True, index=True)
    dislike = Column(Boolean, nullable=True)
    likes = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    post_id = Column(Integer, ForeignKey("post.id"))

    def __init__(self, metadata):
        self.__table__ = metadata.tables[self.__tablename__]
