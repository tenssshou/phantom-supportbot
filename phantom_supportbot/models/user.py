from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from phantom_supportbot.core.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)

    tickets = relationship("Ticket", back_populates="user")
