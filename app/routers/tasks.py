from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import schemas, crud

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

# Database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Task
@router.post("/", response_model=schemas.TaskResponse, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)


# Get All Tasks
@router.get("/", response_model=list[schemas.TaskResponse])
def get_all_tasks(db: Session = Depends(get_db)):
    return crud.get_tasks(db)


# Update Task
@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


# Delete Task
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, task_id)

    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}