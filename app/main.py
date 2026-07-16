from fastapi import FastAPI

from .database import engine, Base
from .routers import tasks

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
    description="Simple Task Management API using FastAPI"
)

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Welcome to Task Manager API"}