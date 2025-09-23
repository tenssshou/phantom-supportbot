from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, ChatMemberUpdatedFilter, IS_ADMIN
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database.crud import CRUD
from app.keyboards.admin import get_admin_keyboard
from app.keyboards.user import get_ticket_actions_keyboard
from app.config import settings

router = Router()


class AnswerTicket(StatesGroup):
    waiting_for_answer = State()


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in settings.ADMIN_USER_IDS:
        await message.answer("❌ Доступ запрещен")
        return

    await message.answer(
        "👨‍💼 Панель администратора:",
        reply_markup=get_admin_keyboard()
    )


@router.callback_query(F.data == "admin_all_tickets")
async def show_all_tickets(callback: CallbackQuery, crud: CRUD):
    tickets = await crud.get_all_tickets()

    if not tickets:
        await callback.message.answer("📭 Тикетов нет")
        return

    text = "📊 Все тикеты:\n\n"
    for ticket in tickets[:10]:  # Ограничиваем вывод
        status_emoji = "🟢" if ticket.status == "open" else "🔵" if ticket.status == "answered" else "🔴"
        text += f"{status_emoji} #{ticket.id} - {ticket.subject} ({ticket.status})\n"

    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data == "admin_open_tickets")
async def show_open_tickets(callback: CallbackQuery, crud: CRUD):
    tickets = await crud.get_open_tickets()

    if not tickets:
        await callback.message.answer("🎉 Нет открытых тикетов!")
        return

    text = "⏳ Открытые тикеты:\n\n"
    for ticket in tickets:
        text += f"🟢 #{ticket.id} - {ticket.subject}\n"

    await callback.message.answer(text)
    await callback.answer()


@router.callback_query(F.data.startswith("answer_"))
async def start_answer_ticket(callback: CallbackQuery, state: FSMContext):
    ticket_id = int(callback.data.split("_")[1])
    await state.set_state(AnswerTicket.waiting_for_answer)
    await state.update_data(ticket_id=ticket_id)

    await callback.message.answer(f"💬 Введите ответ для тикета #{ticket_id}:")
    await callback.answer()


@router.message(AnswerTicket.waiting_for_answer)
async def process_ticket_answer(message: Message, state: FSMContext, crud: CRUD, bot):
    data = await state.get_data()
    ticket_id = data['ticket_id']

    # Добавляем ответ в базу
    await crud.add_message_to_ticket(ticket_id, message.text, True)

    # Получаем информацию о тикете
    ticket = await crud.get_ticket_with_messages(ticket_id)

    # Отправляем ответ пользователю
    await bot.send_message(
        ticket.user.telegram_id,
        f"📨 Ответ по тикету #{ticket_id}:\n\n{message.text}"
    )

    await state.clear()
    await message.answer(f"✅ Ответ на тикет #{ticket_id} отправлен!")