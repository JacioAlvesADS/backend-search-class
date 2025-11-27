from fastapi import APIRouter, HTTPException
from typing import List, Optional
from app.core.database import supabase
from app.schemas.course import CourseResponse

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/", response_model=List[CourseResponse])
async def search_courses(q: Optional[str] = None):
    
    if not q:
        return []

    query_term = f"%{q}%"

    try:
        data = (supabase.table("courses")
                .select("*")
                .or_(f"title.ilike.{query_term},description.ilike.{query_term}")
                .execute())
                
        return data.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na busca: {str(e)}")