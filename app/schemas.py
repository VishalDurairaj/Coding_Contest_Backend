from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# ==========================================
# User Schemas
# ==========================================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "student"  # "student" or "admin"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# ==========================================
# Token Schemas
# ==========================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None


# ==========================================
# Problem Schemas
# ==========================================

class ProblemCreate(BaseModel):
    title: str
    description: str
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None


class ProblemResponse(BaseModel):
    id: int
    contest_id: int
    title: str
    description: str
    input_format: Optional[str] = None
    output_format: Optional[str] = None
    constraints: Optional[str] = None

    class Config:
        from_attributes = True


# ==========================================
# Contest Schemas
# ==========================================

class ContestCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime


class ContestResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    created_by: int
    problems: List[ProblemResponse] = []

    class Config:
        from_attributes = True


# ==========================================
# Submission Schemas
# ==========================================

class SubmissionCreate(BaseModel):
    submitted_code: str
    language: str


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    submitted_code: str
    language: str
    status: str
    submitted_at: datetime

    class Config:
        from_attributes = True