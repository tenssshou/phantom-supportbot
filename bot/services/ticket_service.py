from aiogram import Bot
from app.database.crud import CRUD
from app.config import settings


class TicketService:
    def __init__(self, bot: Bot, crud: CRUD):
        self.bot = bot
        self.crud = crud

    async def notify_admins_about_new_ticket(self, ticket):
        """Уведомление админов о новом тикете"""
        message_text = (
            f"🆕 Новый тикет #{ticket.id}\n"
            f"👤 Пользователь: {ticket.user.first_name} (@{ticket.user.username})\n"
            f"📌 Тема: {ticket.subject}\n"
            f"📄 Описание: {ticket.description}\n\n"
            f"💬 Для ответа используйте /admin"
        )

        await self.bot.send_message(
            settings.ADMIN_GROUP_ID,
            message_text,
            reply_markup=get_ticket_actions_keyboard(ticket.id)
        )

    async def send_open_tickets_reminder(self):
        """Ежечасное уведомление о открытых тикетах"""
        open_tickets = await self.crud.get_open_tickets()

        if open_tickets:
            message_text = f"⏰ Напоминание: {len(open_tickets)} открытых тикетов:\n\n"

            for ticket in open_tickets[:5]:  # Ограничиваем список
                message_text += f"🟢 #{ticket.id} - {ticket.subject}\n"

            if len(open_tickets) > 5:
                message_text += f"\n... и еще {len(open_tickets) - 5} тикетов"

            await self.bot.send_message(
                settings.ADMIN_GROUP_ID,
                message_text,
                reply_markup=get_admin_keyboard()
            )