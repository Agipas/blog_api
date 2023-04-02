from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from post.models import Post


async def get_post_likes_dislikes(like_dislike_numb: int,
                                  like_dislike: Post.likes | Post.dislikes,
                                  session: AsyncSession = Depends(get_async_session)):
    stmt = select(like_dislike).where(Post.id == like_dislike_numb).limit(1)
    result = await session.execute(stmt)
    likes = result.scalar()
    if likes is None:
        return {"status": "error", "message": "Post not found"}
    return likes
