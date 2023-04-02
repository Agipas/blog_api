from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from pydantic import BaseModel

from auth.auth import auth_backend
from auth.models import User
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate

from post.router import routr as router_post
from post.router import create_post
# tags_metadata = [
#     {
#         "name": "users",
#         "description": "Operations with users. The **login** logic is also here.",
#     },
#     {
#         "name": "items",
#         "description": "Manage items. So _fancy_ they have their own docs.",
#         "externalDocs": {
#             "description": "Items external docs",
#             "url": "https://fastapi.tiangolo.com/",
#         },
#     },
# ]

app = FastAPI(title="Blog")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
# current_active_user = fastapi_users.current_user(active=True)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_post)


# @app.post("/create-post")
# async def protected_route( user: User = Depends(current_active_user)):
#     await create_post()
#     return f"Hello, {user.email}"

