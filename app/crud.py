from sqlalchemy.orm import Session
from . import models, schemas

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session):
    return db.query(models.Task).all()

def update_task(db: Session, task_id: int, task: schemas.TaskUpdate):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not db_task:
        return None

    updates = task.model_dump(exclude_unset=True)

    for key, value in updates.items():
        setattr(db_task, key, value)

    db.commit()
    db.refresh(db_task)

    return db_task

def delete_task(db: Session, task_id: int):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if not db_task:
        return None

    db.delete(db_task)
    db.commit()

    return db_task