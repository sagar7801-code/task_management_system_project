from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime
from .db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="open")  # open / completed
    priority = Column(String(20), nullable=False, default="medium")  # low/medium/high
    created_date = Column(DateTime(timezone=False), server_default=func.now())
    due_date = Column(Date, nullable=True)
