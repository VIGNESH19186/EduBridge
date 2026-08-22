from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field(default="student", pattern="^(student|teacher|admin)$")
    preferred_language: Optional[str] = "English"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    name: str
    role: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    preferred_language: str

    class Config:
        from_attributes = True
