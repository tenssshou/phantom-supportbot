import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.core.config import settings
from bot.core.db import engine, Base
from bot.handlers import user, admin, faq
from bot.scheduler.tasks import start_scheduler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.bot_token, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
dp["db"] = engine

async def on_startup():
async with engine.begin() as conn:
await conn.run_sync(Base.metadata.create_all)
start_scheduler()

def include_routers():
dp.include_router(user.router)
dp.include_router(admin.router)
dp.include_router(faq.router)

async def main():
include_routers()
await on_startup()
await dp.start_polling(bot)

if name == "main":
asyncio.run(main())