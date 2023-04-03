from datetime import datetime

from fastapi import Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET
from database import get_async_session

cookie_transport = CookieTransport(cookie_name="blog_cookie", cookie_max_age=3600)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


async def user_logs(session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    stmt = update(User).values(last_request=datetime.utcnow()).where(User.id == user.id)
    await session.execute(stmt)
    await session.commit()
