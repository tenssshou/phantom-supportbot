import asyncio
import logging
from aiohttp import web
from aiogram.types import Update
from phantom_supportbot.core.bot import dp, bot
from phantom_supportbot.core.config import settings
from phantom_supportbot.core.db import init_db
from phantom_supportbot.core.logging import setup_logging
from phantom_supportbot.handlers import users, admins  # noqa
from phantom_supportbot.services.notifier import hourly_unanswered_notifier

setup_logging()
log = logging.getLogger(__name__)

async def handle_webhook(request):
    data = await request.json()
    update = Update(**data)
    await dp.process_update(update)
    return web.Response(text="OK")

async def on_startup(app):
    await init_db()
    await bot.set_webhook(settings.WEBHOOK_URL)
    loop = asyncio.get_event_loop()
    app['notifier_task'] = loop.create_task(hourly_unanswered_notifier(app))

async def on_shutdown(app):
    task = app.get('notifier_task')
    if task:
        task.cancel()
    await bot.delete_webhook()
    await bot.session.close()

def create_app():
    app = web.Application()
    app.router.add_post(f"{settings.WEBHOOK_PATH}/{settings.BOT_TOKEN}", handle_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, host=settings.HOST, port=settings.PORT)
