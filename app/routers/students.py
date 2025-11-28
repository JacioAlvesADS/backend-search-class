from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List
from app.core.database import supabase
from app.core.security import get_current_user
from app.schemas.course import CourseResponse

router = APIRouter(prefix="/users", tags=["Students/Users"])

@router.get("/{user_id}/favoritos", response_model=List[CourseResponse])
async def list_favorites(user_id: UUID, current_user: dict = Depends(get_current_user)):
    if str(user_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a ver favoritos de outro usuário")
        
    try:
        favorites = supabase.table("favorites").select("course_id").eq("user_id", str(user_id)).execute()
        course_ids = [f['course_id'] for f in favorites.data]
        
        if not course_ids:
            return []
            
        courses = supabase.table("courses").select("*").in_("id", course_ids).execute()
        return courses.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{user_id}/favoritos/{course_id}", status_code=200)
async def add_favorite(user_id: UUID, course_id: UUID, current_user: dict = Depends(get_current_user)):
    if str(user_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a alterar favoritos de outro usuário")
        
    uid_str = current_user.id
    cid_str = str(course_id)
    
    try:
        existing = supabase.table("favorites").select("*").eq("user_id", uid_str).eq("course_id", cid_str).execute()
        
        if existing.data:
            raise HTTPException(status_code=400, detail="Curso já está nos favoritos")
        
        supabase.table("favorites").insert({"user_id": uid_str, "course_id": cid_str}).execute()
        return {"message": "Adicionado aos favoritos"}
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco: {str(e)}")

@router.delete("/{user_id}/favoritos/{course_id}", status_code=200)
async def remove_favorite(user_id: UUID, course_id: UUID, current_user: dict = Depends(get_current_user)):
    if str(user_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a alterar favoritos de outro usuário")
        
    uid_str = current_user.id
    cid_str = str(course_id)
    
    try:
        existing = supabase.table("favorites").select("*").eq("user_id", uid_str).eq("course_id", cid_str).execute()
        
        if not existing.data:
            raise HTTPException(status_code=404, detail="Curso não está nos favoritos")
        
        supabase.table("favorites").delete().eq("user_id", uid_str).eq("course_id", cid_str).execute()
        return {"message": "Removido dos favoritos"}
            
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no banco: {str(e)}")

@router.post("/{user_id}/enroll/{course_id}")
async def enroll_course(user_id: UUID, course_id: UUID, current_user: dict = Depends(get_current_user)):
    if str(user_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a matricular outro usuário")
        
    uid_str = current_user.id
    cid_str = str(course_id)
    
    try:
        existing = supabase.table("enrollments").select("*").eq("user_id", uid_str).eq("course_id", cid_str).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Você já está matriculado neste curso")
        
        supabase.table("enrollments").insert({"user_id": uid_str, "course_id": cid_str, "progress": 0}).execute()
        return {"message": "Matrícula realizada com sucesso"}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}/cursos", response_model=List[CourseResponse])
async def get_my_courses(user_id: UUID, current_user: dict = Depends(get_current_user)):
    if str(user_id) != current_user.id:
        raise HTTPException(status_code=403, detail="Não autorizado a ver cursos de outro usuário")
        
    uid_str = current_user.id
    
    try:
        enrollments = supabase.table("enrollments").select("course_id").eq("user_id", uid_str).execute()
        course_ids = [e['course_id'] for e in enrollments.data]
        
        if not course_ids:
            return []
            
        courses = supabase.table("courses").select("*").in_("id", course_ids).execute()
        return courses.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))