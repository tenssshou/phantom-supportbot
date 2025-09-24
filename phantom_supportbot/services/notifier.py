import asyncio
import logging
from phantom_supportbot.core.db import AsyncSessionLocal
from phantom_supportbot.services import crud
from phantom_supportbot.core.bot import bot
from phantom_supportbot.core.config import settings

log = logging.getLogger(__name__)
ADMIN_CHAT = settings.ADMIN_CHAT_ID

async def hourly_unanswered_notifier(app):
    await asyncio.sleep(5)
    while True:
        try:
            async with AsyncSessionLocal() as db:
                tickets = await crud.get_unanswered_tickets(db)
            if tickets:
                lines = [f"#{t.id} {t.title} (user_id={t.user.tg_id if t.user else t.user_id})" for t in tickets[:50]]
                text = "⏳ <b>Неотвеченные тикеты:</b>\n" + "\n".join(lines)
                await bot.send_message(ADMIN_CHAT, text)
        except Exception as e:
            log.exception("Notifier error: %s", e)
        await asyncio.sleep(3600)
