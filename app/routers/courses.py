from fastapi import APIRouter, Depends, HTTPException, status as http_status, UploadFile, File, Form
from typing import List, Optional
from uuid import UUID
from app.core.database import supabase
from app.core.security import get_current_user
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate, CourseStatus
import shutil

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse)
async def create_course(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    status: CourseStatus = Form(CourseStatus.draft),
    thumbnail: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # Check role in profiles table
    try:
        profile_res = supabase.table("profiles").select("role").eq("id", current_user.id).execute()
        if not profile_res.data or profile_res.data[0]['role'] != 'institution':
             raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Only institutions can create courses"
            )
    except Exception as e:
        # If error querying profile (e.g. not found), deny access or re-raise if it's the 403
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to verify user role: {str(e)}")

    try:
        file_content = await thumbnail.read()
        file_path = f"{current_user.id}/{thumbnail.filename}"
        
        res = supabase.storage.from_("course-covers").upload(
            path=file_path,
            file=file_content,
            file_options={"content-type": thumbnail.content_type}
        )
        
        public_url = supabase.storage.from_("course-covers").get_public_url(file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

    course_data = {
        "institution_id": current_user.id,
        "title": title,
        "description": description,
        "price": price,
        "status": status.value,
        "thumbnail_url": public_url
    }

    try:
        data = supabase.table("courses").insert(course_data).execute()
        if not data.data:
             raise HTTPException(status_code=500, detail="Failed to create course record")
        return data.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/", response_model=List[CourseResponse])
async def list_courses(status: Optional[CourseStatus] = None):
    query = supabase.table("courses").select("*")
    if status:
        query = query.eq("status", status.value)
    
    try:
        data = query.execute()
        return data.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(course_id: UUID):
    try:
        data = supabase.table("courses").select("*").eq("id", str(course_id)).execute()
        if not data.data:
            raise HTTPException(status_code=404, detail="Course not found")
        return data.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: UUID,
    course_update: CourseUpdate,
    current_user: dict = Depends(get_current_user)
):
    try:
        existing = supabase.table("courses").select("institution_id").eq("id", str(course_id)).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Course not found")
        if existing.data[0]['institution_id'] != current_user.id:
             raise HTTPException(status_code=403, detail="Not authorized to update this course")
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

    update_data = course_update.model_dump(exclude_unset=True, mode='json')
    
    try:
        data = supabase.table("courses").update(update_data).eq("id", str(course_id)).execute()
        return data.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{course_id}")
async def delete_course(course_id: UUID, current_user: dict = Depends(get_current_user)):
    try:
        existing = supabase.table("courses").select("institution_id").eq("id", str(course_id)).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Course not found")
        if existing.data[0]['institution_id'] != current_user.id:
             raise HTTPException(status_code=403, detail="Not authorized to delete this course")
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
    
    try:
        supabase.table("courses").delete().eq("id", str(course_id)).execute()
        return {"message": "Course deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
