from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from schemas.task import TaskCreate, TaskUpdate, TaskRead
from core.database import get_db
import services.task as task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, data)


@router.get("/", response_model=list[TaskRead])
def get_tasks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return task_service.get_tasks(db, skip, limit)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return task_service.get_task(db, task_id)


@router.patch("/{task_id}", response_model=TaskRead)
def edit_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    return task_service.edit_task(db, task_id, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task_service.delete_task(db, task_id)
