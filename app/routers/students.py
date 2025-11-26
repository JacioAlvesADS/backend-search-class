from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from app.core.database import supabase
from app.core.security import get_current_user
from app.schemas.course import CourseResponse

router = APIRouter(tags=["Students"])

@router.post("/courses/{course_id}/favorite")
async def toggle_favorite(course_id: UUID, current_user: dict = Depends(get_current_user)):
    user_id = current_user.id
    
    try:
        existing = supabase.table("favorites").select("*").eq("user_id", user_id).eq("course_id", str(course_id)).execute()
        
        if existing.data:
            supabase.table("favorites").delete().eq("user_id", user_id).eq("course_id", str(course_id)).execute()
            return {"message": "Removed from favorites"}
        else:
            supabase.table("favorites").insert({"user_id": user_id, "course_id": str(course_id)}).execute()
            return {"message": "Added to favorites"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/courses/{course_id}/enroll")
async def enroll_course(course_id: UUID, current_user: dict = Depends(get_current_user)):
    user_id = current_user.id
    
    try:
        existing = supabase.table("enrollments").select("*").eq("user_id", user_id).eq("course_id", str(course_id)).execute()
        if existing.data:
             raise HTTPException(status_code=400, detail="Already enrolled in this course")
        
        supabase.table("enrollments").insert({"user_id": user_id, "course_id": str(course_id), "progress": 0}).execute()
        return {"message": "Enrolled successfully"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/my-courses", response_model=List[CourseResponse])
async def get_my_courses(current_user: dict = Depends(get_current_user)):
    user_id = current_user.id
    
    try:
        enrollments = supabase.table("enrollments").select("course_id").eq("user_id", user_id).execute()
        course_ids = [e['course_id'] for e in enrollments.data]
        
        if not course_ids:
            return []
            
        courses = supabase.table("courses").select("*").in_("id", course_ids).execute()
        return courses.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
