from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, Base, get_db
import app.models
from app.schemas import UserCreate  # Ensures the models are registered with Base
from app.routes import auth,contests,problems,submissions



# Create all tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Coding Contest Management System",
    description="A lightweight backend for managing contests, problems, and submissions.",
    version="1.0.0"
)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Coding Contest Management Backend",
        "version": "1.0.0"
    }


# Connect the Authentication routes
app.include_router(auth.router)


@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Coding Contest Management Backend",
        "version": "1.0.0"
    }

# Mount Routers
app.include_router(auth.router)
app.include_router(contests.router)


@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Coding Contest Management Backend",
        "version": "1.0.0"
    }

app.include_router(auth.router)
app.include_router(contests.router)
app.include_router(problems.router)


@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Coding Contest Management Backend",
        "version": "1.0.0"
    }

app.include_router(auth.router)
app.include_router(contests.router)
app.include_router(problems.router)
app.include_router(submissions.router)

@app.get("/")
def health_check():
    return {
        "status": "online",
        "system": "Coding Contest Management Backend",
        "version": "1.0.0"
    }