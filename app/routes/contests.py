from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/contests", tags=["Contests"])


@router.post("/", response_model=schemas.ContestResponse, status_code=status.HTTP_201_CREATED)
def create_contest(
    contest_data: schemas.ContestCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_current_admin)
):
    """Admin creates a new coding contest."""
    new_contest = models.Contest(
        title=contest_data.title,
        description=contest_data.description,
        start_time=contest_data.start_time,
        end_time=contest_data.end_time,
        created_by=admin_user.id
    )
    db.add(new_contest)
    db.commit()
    db.refresh(new_contest)
    return new_contest


@router.get("/", response_model=List[schemas.ContestResponse])
def get_all_contests(db: Session = Depends(get_db)):
    """Public: Anyone can view all contests."""
    return db.query(models.Contest).all()


@router.get("/{contest_id}", response_model=schemas.ContestResponse)
def get_contest_by_id(contest_id: int, db: Session = Depends(get_db)):
    """Fetch details of a single contest by its ID."""
    contest = db.query(models.Contest).filter(models.Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} not found"
        )
    return contest


@router.put("/{contest_id}", response_model=schemas.ContestResponse)
def update_contest(
    contest_id: int,
    contest_data: schemas.ContestCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_current_admin)
):
    """Admin updates contest details."""
    contest = db.query(models.Contest).filter(models.Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} not found"
        )

    contest.title = contest_data.title
    contest.description = contest_data.description
    contest.start_time = contest_data.start_time
    contest.end_time = contest_data.end_time

    db.commit()
    db.refresh(contest)
    return contest


@router.delete("/{contest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contest(
    contest_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_current_admin)
):
    """Admin deletes a contest."""
    contest = db.query(models.Contest).filter(models.Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} not found"
        )

    db.delete(contest)
    db.commit()
    return None