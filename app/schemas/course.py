from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from uuid import UUID

class UserRole(str, Enum):
    student = 'student'
    institution = 'institution'

class CourseStatus(str, Enum):
    draft = 'draft'
    published = 'published'
    archived = 'archived'

class ProfileBase(BaseModel):
    display_name: str
    bio: Optional[str] = None
    website: Optional[str] = None

class ProfileResponse(ProfileBase):
    id: UUID
    email: str
    role: UserRole

    class Config:
        from_attributes = True

class CourseBase(BaseModel):
    title: str
    description: str
    price: float
    status: CourseStatus = CourseStatus.draft

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    status: Optional[CourseStatus] = None
    thumbnail_url: Optional[str] = None

class CourseResponse(CourseBase):
    id: UUID
    institution_id: UUID
    thumbnail_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnrollmentBase(BaseModel):
    progress: int = 0

class EnrollmentResponse(EnrollmentBase):
    user_id: UUID
    course_id: UUID
    
    class Config:
        from_attributes = True
