import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.settings import API_TOKEN
from src.handlers import callbacks
from src.handlers import commands
from src.handlers import messages
from src.middlewares import AuthMiddleware


bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(commands.router)
dp.include_router(callbacks.router)
dp.include_router(messages.router)

dp.message.middleware(AuthMiddleware())


async def main():
    logging.basicConfig(level=logging.DEBUG)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
