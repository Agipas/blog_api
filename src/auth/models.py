from datetime import datetime
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    last_request = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    last_login = Column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
