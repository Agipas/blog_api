from datetime import datetime
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions

from auth.models import User
from auth.utils import get_user_db
from config import SECRET


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    # async def on_after_register(self, user: User, request: Optional[Request] = None):
    #     print(f"User {user.username} has registered.")

    async def get_by_email(self, user_email: str) -> models.UP:
        """
        Get a user by e-mail.

        :param user_email: E-mail of the user to retrieve.
        :raises UserNotExists: The user does not exist.
        :return: A user.
        """
        user = await self.user_db.get_by_email(user_email)

        if user is None:
            raise exceptions.UserNotExists()

        return user

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["is_active"] = True
        user_dict["is_verified"] = True
        user_dict["is_superuser"] = False

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)
        return created_user

    async def on_after_login(
        self, user: models.UP, request: Optional[Request] = None
    ) -> None:
        time = datetime.utcnow()
        await self.user_db.update(user, {"last_login": time, "last_request": time})


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

