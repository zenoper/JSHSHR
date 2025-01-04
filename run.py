from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
import logging

import config as Config
from utils.notify_admin import on_startup, on_shutdown
from utils.bot_commands import set_default_commands
from app.middlewares import ThrottlingMiddleware


async def main():
    # Configure logging
    from utils.postgresql import Database
    from app.handlers.start import router
    logging.basicConfig(level=logging.INFO)

    storage = MemoryStorage()
    # Initialize bot and dispatcher
    bot = Bot(token=Config.BOT_TOKEN)

    dp = Dispatcher(storage=storage)
    # Initialize database
    # db = await Database.create()
    # await db.delete_db()
    # await db.init_db()

    await on_startup(bot)
    await set_default_commands(bot)

    # Include the router instance directly
    dp.include_router(router)

    dp.message.outer_middleware(ThrottlingMiddleware(limit=2, interval=1))
    # Start polling
    await dp.start_polling(bot)
    await on_shutdown(bot)

if __name__ == "__main__":
    asyncio.run(main())
