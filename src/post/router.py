from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session
from post.models import Post
from post.schemas import PostCreate
from auth.auth import current_user

routr = APIRouter(
    prefix="/post",
    tags=["Post"]
)


async def get_post_likes_dislikes(like_dislike_numb: int,
                                  like_dislike: Post.likes | Post.dislikes,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = select(like_dislike).where(Post.id == like_dislike_numb).limit(1)
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
    likes = await get_post_likes_dislikes(post_id, Post.likes, session)
    if not isinstance(likes, int):
        return likes
    likes += 1
    stmt = update(Post).values(likes=likes, updated_at=datetime.utcnow()).where(Post.id == post_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@routr.post("/unlike_post/{post_id}")
async def unlike_post(post_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    dislikes = await get_post_likes_dislikes(post_id, Post.dislikes, session)
    if not isinstance(dislikes, int):
        return dislikes
    dislikes += 1
    stmt = update(Post).values(dislikes=dislikes, updated_at=datetime.utcnow()).where(Post.id == post_id)
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
