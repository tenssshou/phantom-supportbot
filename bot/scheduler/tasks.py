from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession
from bot.crud import ticket as crud
from bot.core.config import settings
from bot.main import bot

scheduler = AsyncIOScheduler()

async def remind_open_tickets():
async with AsyncSession(bind=bot["db"]) as session:
rows = await crud.list_open_tickets(session)
if not rows:
return
text = "⏳ Неотвеченные тикеты:\n" + "\n".join(
f"#{t.id} от @{t.username or 'скрыт'}" for t in rows
)
await bot.send_message(settings.admin_group_id, text)

def start_scheduler():
scheduler.add_job(remind_open_tickets, "interval", seconds=settings.remind_interval)
scheduler.start()