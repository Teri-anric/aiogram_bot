from typing import List

from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InputMediaPhoto, InputMediaVideo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from bot.db import Post, PostMedia
from bot.config_reader import config

router = Router(name="send-post-router")
router.message.filter(F.chat.id == config.chat_id)


@router.message(F.chat.type == 'supergroup')
async def handler_send_post(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    count = data.get('count', 0)
    count = 0 if count > 1 else count + 1
    await state.update_data(count=count)
    if count:
        return
    await send_post(message, session)

async def send_post(message: Message, session: AsyncSession):
    # get post from db
    result = await session.execute(select(Post))
    post: Post = result.scalar()
    result = await session.execute(select(PostMedia).filter_by(post_id=post.id))
    post_media: List[PostMedia] = result.scalars()
    media = []
    # convert media
    for m in post_media:
        if m.type_media == InputMediaType.PHOTO:
            media.append(InputMediaPhoto(media=m.tg_file_id))
        elif m.type_media == InputMediaType.VIDEO:
            media.append(InputMediaVideo(media=m.tg_file_id))
    # send
    if not media:
        await message.answer(post.title)
    else:
        media[0].caption = post.title
        await message.answer_media_group(media=media)
    # delete post
    await session.delete(post)
    await session.commit()
