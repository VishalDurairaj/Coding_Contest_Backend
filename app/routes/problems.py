from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, auth

router = APIRouter(tags=["Problems"])


@router.post(
    "/contests/{contest_id}/problems",
    response_model=schemas.ProblemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_problem(
    contest_id: int,
    problem_data: schemas.ProblemCreate,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_current_admin)
):
    """Admin creates a new problem for a given contest."""
    contest = db.query(models.Contest).filter(models.Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} does not exist"
        )

    new_problem = models.Problem(
        contest_id=contest_id,
        title=problem_data.title,
        description=problem_data.description,
        input_format=problem_data.input_format,
        output_format=problem_data.output_format,
        constraints=problem_data.constraints
    )
    db.add(new_problem)
    db.commit()
    db.refresh(new_problem)
    return new_problem


@router.get("/contests/{contest_id}/problems", response_model=List[schemas.ProblemResponse])
def get_problems_by_contest(contest_id: int, db: Session = Depends(get_db)):
    """List all problems belonging to a contest."""
    contest = db.query(models.Contest).filter(models.Contest.id == contest_id).first()
    if not contest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contest with ID {contest_id} does not exist"
        )
    return contest.problems


@router.get("/problems/{problem_id}", response_model=schemas.ProblemResponse)
def get_problem_by_id(problem_id: int, db: Session = Depends(get_db)):
    """View single problem details."""
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID {problem_id} not found"
        )
    return problem


@router.delete("/problems/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_problem(
    problem_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(auth.get_current_admin)
):
    """Admin deletes a problem."""
    problem = db.query(models.Problem).filter(models.Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Problem with ID {problem_id} not found"
        )

    db.delete(problem)
    db.commit()
    return None