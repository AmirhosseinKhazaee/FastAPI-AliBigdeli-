from sqlalchemy.orm import Session
from models.task import TaskModel
from schemas.task import *
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


def create_task(db: Session, data: TaskCreate):
    task_db = TaskModel(**data.model_dump())
    db.add(task_db)
    db.commit()
    db.refresh(task_db)
    return task_db


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(TaskModel).offset(skip).limit(limit).all()


def get_task(db: Session, id: int):
    task_db = db.get(TaskModel, id)

    if task_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task_db


def edit_task(db: Session, id: int, data: TaskUpdate):
    task_db = get_task(db=db, id=id)

    update_data = data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in update_data.items():
        setattr(task_db, key, value)

    db.commit()
    db.refresh(task_db)

    return task_db


def delete_task(db: Session, id: int):
    task_db = get_task(db=db, id=id)

    db.delete(task_db)
    db.commit()
