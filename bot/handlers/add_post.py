from typing import List

from aiogram import Router, F
from aiogram.enums import ContentType, InputMediaType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db import Post, PostMedia
from bot.status import InputPostStates
from bot.config_reader import config

router = Router(name="add-post-router")
router.message.filter(F.chat.id == config.admin_id)


@router.message(Command("add_post"))
async def cmd_add_post(message: Message, state: FSMContext):
    await message.answer("Ведіть текст поста")
    await state.set_state(InputPostStates.in_text)


@router.message(InputPostStates.in_text)
async def in_title_post(message: Message, state: FSMContext):
    await message.answer("Відправте фото/відео поста")
    await state.update_data(post_title=message.text)
    await state.set_state(InputPostStates.in_photo)


@router.message(InputPostStates.in_photo, F.media_group_id)
async def in_photo_post(message: Message, state: FSMContext, album: List[Message], session: AsyncSession):
    data = await state.get_data()
    post = Post(title=data.get('post_title'), media=[])
    # add media to post
    for item in album:
        file_id = None
        media_type = None

        if item.content_type == ContentType.PHOTO:
            file_id = item.photo[-1].file_id
            media_type = InputMediaType.PHOTO
        elif item.content_type == ContentType.VIDEO:
            file_id = item.video.file_id
            media_type = InputMediaType.VIDEO

        post.media.append(PostMedia(tg_file_id=file_id, type_media=media_type))

    session.add(post)
    await session.commit()

    await message.answer("Готово")
    await state.clear()
