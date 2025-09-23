from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.database.crud import CRUD
from app.keyboards.user import get_main_keyboard, get_faq_keyboard

router = Router()


class TicketCreation(StatesGroup):
    waiting_for_subject = State()
    waiting_for_description = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в службу поддержки!\n\n"
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "📋 Создать тикет")
async def create_ticket_start(message: Message, state: FSMContext):
    await state.set_state(TicketCreation.waiting_for_subject)
    await message.answer("📝 Введите тему тикета:")


@router.message(TicketCreation.waiting_for_subject)
async def process_subject(message: Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(TicketCreation.waiting_for_description)
    await message.answer("📄 Теперь опишите вашу проблему подробно:")


@router.message(TicketCreation.waiting_for_description)
async def process_description(message: Message, state: FSMContext, crud: CRUD):
    data = await state.get_data()
    user = await crud.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    ticket = await crud.create_ticket(
        user_id=user.id,
        subject=data['subject'],
        description=message.text
    )

    await state.clear()
    await message.answer(
        f"✅ Тикет #{ticket.id} создан!\n"
        f"Тема: {ticket.subject}\n"
        f"Ожидайте ответа от поддержки.",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "❓ FAQ")
async def show_faq(message: Message):
    await message.answer(
        "❓ Часто задаваемые вопросы:",
        reply_markup=get_faq_keyboard()
    )


@router.message(F.text == "📊 История тикетов")
async def show_ticket_history(message: Message, crud: CRUD):
    user = await crud.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    tickets = await crud.get_user_tickets(user.id)

    if not tickets:
        await message.answer("📭 У вас пока нет тикетов.")
        return

    for ticket in tickets:
        status_emoji = "🟢" if ticket.status == "open" else "🔵" if ticket.status == "answered" else "🔴"
        await message.answer(
            f"{status_emoji} Тикет #{ticket.id}\n"
            f"📌 Тема: {ticket.subject}\n"
            f"📅 Создан: {ticket.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"📊 Статус: {ticket.status}"
        )


@router.callback_query(F.data.startswith("faq_"))
async def process_faq(callback: CallbackQuery):
    faq_type = callback.data.split("_")[1]

    faq_texts = {
        "create": "📝 Чтобы создать тикет:\n1. Нажмите 'Создать тикет'\n2. Введите тему\n3. Опишите проблему",
        "time": "⏱️ Ответ в течение 24 часов\nВ рабочее время: 1-4 часа",
        "cancel": "❌ Напишите в поддержку для отмены тикета"
    }

    await callback.message.edit_text(
        faq_texts.get(faq_type, "Информация не найдена"),
        reply_markup=get_faq_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "👋 Добро пожаловать в службу поддержки!\n\nВыберите действие:"
    )
    await callback.answer()