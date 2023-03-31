from datetime import datetime
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("registered_at", TIMESTAMP),
    Column("last_request", TIMESTAMP),
    Column("last_login", TIMESTAMP),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=True, nullable=False), # default was False
)

post = Table(
    "post",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("text", String, nullable=False),
    Column("likes", Integer, default=0),
    Column("created_at", TIMESTAMP, default=datetime.utcnow),
    Column("updated_at", TIMESTAMP, default=datetime.utcnow),
    Column("user_id", Integer, ForeignKey(user.c.id), nullable=False)
)
