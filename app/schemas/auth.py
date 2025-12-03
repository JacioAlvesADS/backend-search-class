from pydantic import BaseModel, EmailStr, Field
from app.schemas.course import UserRole

class UserSignup(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    display_name: str
    role: UserRole = UserRole.student

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict
