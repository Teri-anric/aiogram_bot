import asyncio
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.strategy import FSMStrategy
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config_reader import config
from bot.db import Base
from bot.handlers import commands, add_post, chat
from bot.middlewares import DbSessionMiddleware, MediaGroupMiddleware


async def main():
    # setup database
    engine = create_async_engine(url=config.db_url)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")

    # Setup dispatcher and bind routers to it
    dp = Dispatcher(fsm_strategy=FSMStrategy.CHAT)
    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    dp.message.middleware(MediaGroupMiddleware())

    # Register handlers
    dp.include_router(commands.router)
    dp.include_router(add_post.router)
    dp.include_router(chat.router)

    # Run bot
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    Base.metadata.create_all(create_engine(url=config.db_url))
    # fix
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
