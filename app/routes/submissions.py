from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(tags=["Submissions"])


@router.post(
    "/problems/{problem_id}/submit",
    response_model=schemas.SubmissionResponse,
    status_code=status.HTTP_201_CREATED
)
def submit_code(
    problem_id: int,
    submission_data: schemas.SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Authenticated student or admin submits solution code."""
    # 1. Verify the problem exists
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID {problem_id} does not exist"
        )

    # 2. Persist submission with initial status 'Pending'
    new_submission = models.Submission(
        user_id=current_user.id,
        problem_id=problem_id,
        submitted_code=submission_data.submitted_code,
        language=submission_data.language.lower(),
        status="Pending"
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission


@router.get("/submissions/my", response_model=List[schemas.SubmissionResponse])
def get_my_submissions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Students/Users view only their own submissions."""
    return db.query(models.Submission).filter(
        models.Submission.user_id == current_user.id
    ).all()


@router.get("/submissions", response_model=List[schemas.SubmissionResponse])
def get_all_submissions(
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_current_admin)
):
    """Admin-only: View every submission from all users."""
    return db.query(models.Submission).all()