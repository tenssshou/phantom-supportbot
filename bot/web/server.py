from aiohttp import web
from aiogram import Bot
from app.config import settings


async def handle_webhook(request):
    bot: Bot = request.app['bot']
    data = await request.json()
    update = Update(**data)
    await bot.process_update(update)
    return web.Response()


async def create_webhook_app(bot, dispatcher):
    app = web.Application()
    app['bot'] = bot

    app.router.add_post(settings.WEBHOOK_PATH, handle_webhook)
    return app