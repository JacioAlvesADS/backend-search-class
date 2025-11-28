from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class InstitutionResponse(BaseModel):
    id: UUID
    display_name: Optional[str] = None
    bio: Optional[str] = None
    website: Optional[str] = None
    
    class Config:
        from_attributes = True