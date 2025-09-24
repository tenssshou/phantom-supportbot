import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from phantom_supportbot.core.config import settings

log = logging.getLogger(__name__)

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())
