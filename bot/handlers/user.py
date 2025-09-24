from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from bot.crud import ticket as crud
from bot.models.ticket import Ticket
from bot.keyboards.inline import kb_faq, kb_cancel

router = Router()

class NewTicket(StatesGroup):
text = State()

@router.message(Command("start"))
async def cmd_start(m: Message):
await m.answer(
"👋 Привет! Выбери действие:",
reply_markup=kb_faq()
)

@router.callback_query(F.data == "new_ticket")
async def new_ticket(clb: CallbackQuery, state: FSMContext):
await clb.message.edit_text("Опишите вашу проблему:", reply_markup=kb_cancel())
await state.set_state(NewTicket.text)

@router.message(NewTicket.text)
async def save_ticket(m: Message, state: FSMContext, session: AsyncSession):
await state.clear()
t = await crud.create_ticket(
session, m.from_user.id, m.from_user.username or "", m.text
)
await m.answer(f"✅ Тикет #{t.id} создан. Ответ придёт сюда же.")
# отправляем в группу админов
from bot.main import bot
from bot.core.config import settings
await bot.send_message(
settings.admin_group_id,
f"🔔 Новый тикет #{t.id} от @{m.from_user.username or 'скрыт'}:\n\n{m.text}"
)

@router.callback_query(F.data == "my_tickets")
async def my_tickets(clb: CallbackQuery, session: AsyncSession):
rows = await crud.list_user_tickets(session, clb.from_user.id)
if not rows:
await clb.message.edit_text("У вас пока нет тикетов.")
return
text = "\n\n".join(
f"#{t.id} — {t.status.value}\n{t.text[:100]}"
+ (f"\nОтвет: {t.answer}" if t.answer else "")
for t in rows
)
await clb.message.edit_text(text)

