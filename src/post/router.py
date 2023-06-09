from datetime import datetime, date

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session
from post.models import Post, PostLogs
from post.schemas import PostCreate
from auth.auth import current_user, user_logs
from post.utils import get_post_likes_dislikes

routr = APIRouter(
    prefix="/post",
    tags=["Post"]
)


@routr.get("/all/")
async def get_all_posts(session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_user)):
    await user_logs(session, user)
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return posts


@routr.post("/")
async def create_post(new_post: PostCreate,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    await user_logs(session, user)
    new_post.user_id = user.id
    stmt = insert(Post).values(**new_post.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@routr.post("/like_post/{post_id}")
async def like_post(post_id: int,
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_user)):
    await user_logs(session, user)
    likes = await get_post_likes_dislikes(post_id, Post.likes, session)
    if not isinstance(likes, int):
        return likes
    likes += 1
    stmt = update(Post).values(likes=likes, updated_at=datetime.utcnow()).where(Post.id == post_id)
    await session.execute(stmt)
    stmt = insert(PostLogs).values(likes=True, created_at=datetime.utcnow(), post_id=post_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@routr.post("/unlike_post/{post_id}")
async def unlike_post(post_id: int,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    await user_logs(session, user)
    dislikes = await get_post_likes_dislikes(post_id, Post.dislikes, session)
    if not isinstance(dislikes, int):
        return dislikes
    dislikes += 1
    stmt = update(Post).values(dislikes=dislikes, updated_at=datetime.utcnow()).where(Post.id == post_id)
    await session.execute(stmt)
    stmt = insert(PostLogs).values(dislikes=True, created_at=datetime.utcnow(), post_id=post_id)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@routr.get("/")
async def get_users_posts(session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    await user_logs(session, user)
    query = select(Post).where(Post.user_id == user.id)
    result = await session.execute(query)
    posts = result.scalars().all()
    return posts


@routr.get("/analytics/")
async def get_posts_analytics(date_from: date,
                              date_to: date,
                              session: AsyncSession = Depends(get_async_session),
                              user: User = Depends(current_user)):
    await user_logs(session, user)
    query = select(func.date(PostLogs.created_at).label('day'),
                   func.count(PostLogs.id).label('count')) \
        .where((date_from < PostLogs.created_at) & (PostLogs.created_at < date_to)) \
        .group_by(func.date(PostLogs.created_at))
    result = await session.execute(query)
    posts = result.all()
    return [{post[0]: post[1]} for post in posts]


@routr.get("/get_last_post/")
async def get_last_post(session: AsyncSession = Depends(get_async_session),
                          user: User = Depends(current_user)):
    await user_logs(session, user)
    query = select(Post.id).order_by(Post.id.desc()).limit(1)
    result = await session.execute(query)
    last_post = result.scalars().all()
    return last_post
