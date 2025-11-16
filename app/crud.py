from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from . import models, schemas


def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(
        title=task_in.title,
        description=task_in.description,
        priority=task_in.priority,
        due_date=task_in.due_date,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def list_tasks(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_before: Optional[date] = None,
    due_after: Optional[date] = None,
) -> List[models.Task]:
    q = db.query(models.Task)
    if status:
        q = q.filter(models.Task.status == status)
    if priority:
        q = q.filter(models.Task.priority == priority)
    if due_before:
        q = q.filter(models.Task.due_date != None).filter(
            models.Task.due_date <= due_before
        )
    if due_after:
        q = q.filter(models.Task.due_date != None).filter(
            models.Task.due_date >= due_after
        )
    return q.order_by(models.Task.created_date.desc()).all()


def update_task(
    db: Session, db_task: models.Task, task_in: schemas.TaskUpdate
) -> models.Task:
    if task_in.title is not None:
        db_task.title = task_in.title
    if task_in.description is not None:
        db_task.description = task_in.description
    if task_in.priority is not None:
        db_task.priority = task_in.priority
    if task_in.due_date is not None:
        db_task.due_date = task_in.due_date
    if task_in.status is not None:
        db_task.status = task_in.status

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: models.Task) -> None:
    db.delete(db_task)
    db.commit()


def set_status(db: Session, db_task: models.Task, status: str) -> models.Task:
    db_task.status = status
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
