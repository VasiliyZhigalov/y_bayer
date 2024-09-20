import logging
import sys
from pathlib import Path

# Добавляем корневую директорию проекта в sys.path
src_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(src_dir))

from aiogram import Bot, Dispatcher

from src.containers import AppContainer
from src.api.bot_handlers import router
from src.api.service_handlers import service_router

from src.api import bot_handlers

from src.orm.base import Base

container = AppContainer()

logging.basicConfig(level=logging.INFO)

bot = container.bot()
dp = container.dispatcher()


async def main():
    db_engine = container.engine()

    dp.include_router(service_router)
    dp.include_router(router)

    Base.metadata.create_all(db_engine)
    await  dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    container.init_resources()
    container.wire(modules=[__name__, 'src.api.bot_handlers', 'src.api.service_handlers'])
    asyncio.run(main())
