from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from bot.models.ticket import Ticket, Status

async def create_ticket(
session: AsyncSession, user_id: int, username: str, text: str
) -> Ticket:
t = Ticket(user_id=user_id, username=username, text=text)
session.add(t)
await session.commit()
await session.refresh(t)
return t

async def get_ticket(session: AsyncSession, ticket_id: int) -> Ticket | None:
return await session.get(Ticket, ticket_id)

async def list_user_tickets(session: AsyncSession, user_id: int):
res = await session.scalars(
select(Ticket).where(Ticket.user_id == user_id).order_by(Ticket.created_at.desc())
)
return res.all()

async def list_open_tickets(session: AsyncSession):
res = await session.scalars(
select(Ticket).where(Ticket.status == Status.open).order_by(Ticket.created_at)
)
return res.all()

async def answer_ticket(
session: AsyncSession, ticket_id: int, answer: str, admin: str
):
await session.execute(
update(Ticket)
.where(Ticket.id == ticket_id)
.values(status=Status.answered, answer=answer, answered_by=admin)
)
await session.commit()