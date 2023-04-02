from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session
# from post.models import post, Post
from post.models import Post
from post.schemas import PostCreate, LikePost
from auth.auth import current_user

routr = APIRouter(
    prefix="/post",
    tags=["Post"]
)


async def get_post_likes(liked_post: int,
                         session: AsyncSession = Depends(get_async_session), ):
    stmt = select(Post.likes).where(Post.id == liked_post).limit(1)
    result = await session.execute(stmt)
    likes = result.scalar()
    if likes is None:
        return {"status": "error", "message": "Post not found"}
    return likes


@routr.post("/")
async def create_post(new_post: PostCreate,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    new_post.user_id = user.id
    stmt = insert(Post).values(**new_post.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@routr.post("/like_post/{post_id}")
async def like_post(post_id: int,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    likes = await get_post_likes(post_id, session)
    if not isinstance(likes, int):
        return likes
    likes += 1
    stmt = update(Post).values(likes=likes, updated_at=datetime.utcnow()).where(Post.id == post_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@routr.post("/unlike_post/{post_id}")
async def like_post(post_id: int,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    print(post_id)
    likes = await get_post_likes(post_id, session)
    if not isinstance(likes, int):
        return likes
    likes -= 1
    stmt = update(Post).values(likes=likes, updated_at=datetime.utcnow()).where(Post.id == post_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@routr.get("/")
async def get_users_posts(session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    query = select(Post).where(Post.user_id == user.id)
    result = await session.execute(query)
    posts = result.scalars().all()
    return posts
