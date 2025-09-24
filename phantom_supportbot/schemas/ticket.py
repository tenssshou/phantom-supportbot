from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketCreate(BaseModel):
    title: str
    description: str

class TicketOut(BaseModel):
    id: int
    title: str
    description: str
    created_at: datetime
    answered: bool
    answered_at: Optional[datetime]

    class Config:
        orm_mode = True
