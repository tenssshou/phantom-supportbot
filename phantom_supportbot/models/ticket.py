from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from phantom_supportbot.core.db import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    answered = Column(Boolean, default=False, nullable=False)
    admin_msg_id = Column(Integer, nullable=True)
    admin_chat_id = Column(Integer, nullable=True)
    answered_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="tickets")
