# Refrence from: https://fastapi.tiangolo.com/tutorial/body-fields/

from typing import Optional
from pydantic import BaseModel, Field, validator
from datetime import date, datetime


VALID_PRIORITIES = {"low", "medium", "high"}
VALID_STATUS = {"open", "completed"}


class TaskBase(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field("medium")
    due_date: Optional[date] = None

    @validator("priority")
    def check_priority(cls, v):
        if v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
        return v


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None

    @validator("priority")
    def check_priority(cls, v):
        if v is None:
            return v
        if v not in VALID_PRIORITIES:
            raise ValueError(f"priority must be one of {VALID_PRIORITIES}")
        return v

    @validator("status")
    def check_status(cls, v):
        if v is None:
            return v
        if v not in VALID_STATUS:
            raise ValueError(f"status must be one of {VALID_STATUS}")
        return v


class TaskOut(TaskBase):
    id: int
    status: str
    created_date: Optional[datetime]

    class Config:
        orm_mode = True
