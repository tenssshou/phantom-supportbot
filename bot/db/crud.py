from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, desc
from app.database.models import User, Ticket, TicketMessage


class CRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, telegram_id: int, username: str, first_name: str, last_name: str = None):
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)

        return user

    async def create_ticket(self, user_id: int, subject: str, description: str):
        ticket = Ticket(
            user_id=user_id,
            subject=subject,
            description=description
        )
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)

        # Создаем первое сообщение от пользователя
        message = TicketMessage(
            ticket_id=ticket.id,
            from_admin=False,
            message_text=description
        )
        self.session.add(message)
        await self.session.commit()

        return ticket

    async def get_user_tickets(self, user_id: int):
        result = await self.session.execute(
            select(Ticket).where(Ticket.user_id == user_id).order_by(desc(Ticket.created_at))
        )
        return result.scalars().all()

    async def get_open_tickets(self):
        result = await self.session.execute(
            select(Ticket).where(Ticket.status == "open").order_by(Ticket.created_at)
        )
        return result.scalars().all()

    async def get_all_tickets(self):
        result = await self.session.execute(
            select(Ticket).order_by(desc(Ticket.created_at))
        )
        return result.scalars().all()

    async def add_message_to_ticket(self, ticket_id: int, message_text: str, from_admin: bool):
        message = TicketMessage(
            ticket_id=ticket_id,
            from_admin=from_admin,
            message_text=message_text
        )
        self.session.add(message)

        if from_admin:
            await self.session.execute(
                update(Ticket)
                .where(Ticket.id == ticket_id)
                .values(status="answered", answered_at=func.now())
            )

        await self.session.commit()
        return message

    async def get_ticket_with_messages(self, ticket_id: int):
        result = await self.session.execute(
            select(Ticket).where(Ticket.id == ticket_id)
        )
        return result.scalar_one_or_none()