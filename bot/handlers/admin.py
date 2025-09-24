from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession
from bot.crud import ticket as crud
from bot.core.config import settings
from bot.models.ticket import Status

router = Router()

@router.message(
F.chat.id == settings.admin_group_id,
F.reply_to_message,
F.content_type == "text"
)
async def answer_ticket(m: Message, session: AsyncSession):
# достаём номер тикета из текста оригинального сообщения
try:
ticket_id = int(m.reply_to_message.text.split("#")[1].split()[0])
except Exception:
return
t = await crud.get_ticket(session, ticket_id)
if not t or t.status != Status.open:
await m.reply("Тикет закрыт или не найден.")
return
await crud.answer_ticket(session, ticket_id, m.text, m.from_user.username or "admin")
from bot.main import bot
await bot.send_message(
t.user_id,
f"💬 Ответ на тикет #{ticket_id}:\n\n{m.text}"
)
await m.reply("✅ Ответ отправлен пользователю.")