import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings
from app.database.base import Base
from app.database.crud import CRUD
from app.handlers import users, admin
from app.services.ticket_service import TicketService
from app.web.server import create_webhook_app

logging.basicConfig(level=logging.INFO)


async def main():
    # Инициализация бота и диспетчера
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Подключение к базе данных
    engine = create_async_engine(
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    # Создание таблиц
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Регистрация роутеров
    dp.include_router(users.router)
    dp.include_router(admin.router)

    # Dependency injection
    async def get_crud():
        async with async_session() as session:
            yield CRUD(session)

    dp["crud"] = get_crud

    # Запуск вебхуков или поллинга
    if settings.WEBHOOK_URL:
        # Настройка вебхуков
        webhook_url = f"{settings.WEBHOOK_URL}{settings.WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url)

        app = await create_webhook_app(bot, dp)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, settings.WEB_SERVER_HOST, settings.WEB_SERVER_PORT)
        await site.start()

        logging.info(f"Webhook server started on {settings.WEB_SERVER_HOST}:{settings.WEB_SERVER_PORT}")

        # Бесконечный цикл для поддержания работы
        await asyncio.Future()
    else:
        # Запуск поллинга
        await bot.delete_webhook()
        await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())