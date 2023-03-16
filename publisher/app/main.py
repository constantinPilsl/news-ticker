import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram_dialog import DialogRegistry
from publisher.config.config import Config

from publisher.events.event_handler import EventHandler
from publisher.views.dialog import dialog

config = Config()


async def main():
    storage = MemoryStorage()
    bot = Bot(token=config.API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    dp.register_message_handler(EventHandler.start, text="/start", state="*")
    registry = DialogRegistry(dp)
    registry.register(dialog)

    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
