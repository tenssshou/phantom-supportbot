from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from phantom_supportbot.models import user, ticket

User = user.User
Ticket = ticket.Ticket

async def get_or_create_user(db: AsyncSession, tg_id: int, name: str = None):
    q = await db.execute(select(User).where(User.tg_id == tg_id))
    u = q.scalars().first()
    if u:
        return u
    u = User(tg_id=tg_id, name=name)
    db.add(u)
    await db.commit()
    await db.refresh(u)
    return u

async def create_ticket(db: AsyncSession, u: User, title: str, description: str):
    t = Ticket(user_id=u.id, title=title, description=description)
    db.add(t)
    await db.commit()
    await db.refresh(t)
    return t

async def set_ticket_admin_message(db: AsyncSession, ticket_id: int, admin_msg_id: int, admin_chat_id: int):
    await db.execute(
        update(Ticket)
        .where(Ticket.id == ticket_id)
        .values(admin_msg_id=admin_msg_id, admin_chat_id=admin_chat_id)
    )
    await db.commit()

async def mark_ticket_answered(db: AsyncSession, ticket_id: int):
    await db.execute(
        update(Ticket)
        .where(Ticket.id == ticket_id)
        .values(answered=True, answered_at=datetime.utcnow())
    )
    await db.commit()

async def get_user_tickets(db: AsyncSession, user_id: int):
    q = await db.execute(select(Ticket).where(Ticket.user_id == user_id).order_by(Ticket.created_at.desc()))
    return q.scalars().all()

async def get_all_tickets(db: AsyncSession):
    q = await db.execute(select(Ticket).order_by(Ticket.created_at.desc()))
    return q.scalars().all()

async def get_unanswered_tickets(db: AsyncSession):
    q = await db.execute(select(Ticket).where(Ticket.answered == False).order_by(Ticket.created_at.asc()))
    return q.scalars().all()

async def get_ticket_by_admin_msg(db: AsyncSession, admin_msg_id: int, admin_chat_id: int):
    q = await db.execute(select(Ticket).where(Ticket.admin_msg_id == admin_msg_id, Ticket.admin_chat_id == admin_chat_id))
    return q.scalars().first()
