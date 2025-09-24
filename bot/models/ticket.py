import enum
from datetime import datetime
from sqlalchemy import (
BigInteger, Column, DateTime, Enum, Integer, String, Text
)
from bot.core.db import Base

class Status(enum.Enum):
open = "open"
answered = "answered"
closed = "closed"

class Ticket(Base):
tablename = "tickets"

id = Column(Integer, primary_key=True)
user_id = Column(BigInteger, nullable=False)
username = Column(String(128))
text = Column(Text, nullable=False)
status = Column(Enum(Status), default=Status.open)
created_at = Column(DateTime, default=datetime.utcnow)
answer = Column(Text)
answered_by = Column(String(128))