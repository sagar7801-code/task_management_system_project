# Reference from : https://fastapi.tiangolo.com/tutorial/sql-databases/
# Reference from : https://fastapi.tiangolo.com/tutorial/first-steps/

from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from . import models, schemas, crud
from .db import engine, SessionLocal, Base

# create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks", response_model=schemas.TaskOut, status_code=201)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    # simple extra validation: due_date cannot be before today
    if task_in.due_date is not None and task_in.due_date < date.today():
        raise HTTPException(status_code=400, detail="due_date cannot be in the past")
    task = crud.create_task(db, task_in)
    return task


@app.get("/tasks", response_model=List[schemas.TaskOut])
def read_tasks(
    status: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    due_before: Optional[date] = Query(None),
    due_after: Optional[date] = Query(None),
    db: Session = Depends(get_db),
):
    tasks = crud.list_tasks(
        db, status=status, priority=priority, due_before=due_before, due_after=due_after
    )
    return tasks


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(
    task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)
):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    # if due_date present validate
    if task_in.due_date is not None and task_in.due_date < date.today():
        raise HTTPException(status_code=400, detail="due_date cannot be in the past")
    updated = crud.update_task(db, task, task_in)
    return updated


@app.patch("/tasks/{task_id}/status", response_model=schemas.TaskOut)
def change_status(
    task_id: int, status: str = Query(...), db: Session = Depends(get_db)
):
    if status not in {"open", "completed"}:
        raise HTTPException(
            status_code=400, detail="status must be 'open' or 'completed'"
        )
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    new_task = crud.set_status(db, task, status)
    return new_task


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return None
