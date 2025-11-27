from fastapi import APIRouter, Depends, HTTPException, status as http_status, UploadFile, File, Form
from typing import List, Optional
from uuid import UUID
from app.core.database import supabase
from app.core.security import get_current_user
from app.schemas.course import CourseCreate, CourseResponse, CourseUpdate, CourseStatus
import shutil

router = APIRouter(prefix="/programas", tags=["Programas (Cursos)"])

@router.get("/destaque", response_model=List[CourseResponse])
async def get_highlight_courses():
    try:
        data = supabase.table("courses").select("*").order("created_at", desc=True).limit(3).execute()
        return data.data
    except Exception as e:
        print(f"Erro destaques: {e}")
        return []

@router.get("/populares", response_model=List[CourseResponse])
async def get_popular_courses():
    try:
        data = supabase.table("courses").select("*").limit(5).execute()
        return data.data
    except Exception as e:
        return []

@router.get("/recentes", response_model=List[CourseResponse])
async def get_recent_courses():
    try:
        data = supabase.table("courses").select("*").order("created_at", desc=True).limit(10).execute()
        return data.data
    except Exception as e:
        return []

@router.get("/categoria/{area}", response_model=List[CourseResponse])
async def get_courses_by_category(area: str):
    try:
        data = supabase.table("courses").select("*").ilike("description", f"%{area}%").execute()
        return data.data
    except Exception as e:
        return []


@router.post("/", response_model=CourseResponse)
async def create_course(
    title: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    status: CourseStatus = Form(CourseStatus.draft),
    thumbnail: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    try:
        profile_res = supabase.table("profiles").select("role").eq("id", current_user.id).execute()
        if not profile_res.data or profile_res.data[0]['role'] != 'institution':
             raise HTTPException(
                status_code=http_status.HTTP_403_FORBIDDEN,
                detail="Apenas instituições podem criar cursos."
            )
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=f"Erro ao verificar permissão: {str(e)}")

    # Upload da Imagem
    try:
        file_content = await thumbnail.read()
        file_path = f"{current_user.id}/{thumbnail.filename}"
        
        supabase.storage.from_("course-covers").upload(
            path=file_path,
            file=file_content,
            file_options={"content-type": thumbnail.content_type, "x-upsert": "true"}
        )
        
        public_url = supabase.storage.from_("course-covers").get_public_url(file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload da imagem: {str(e)}")

    # Salvar no Banco
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
             raise HTTPException(status_code=500, detail="Falha ao criar registro do curso")
        return data.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de banco de dados: {str(e)}")

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
            raise HTTPException(status_code=404, detail="Curso não encontrado")
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
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        if existing.data[0]['institution_id'] != current_user.id:
             raise HTTPException(status_code=403, detail="Sem permissão para editar este curso")
    except Exception as e:
         if isinstance(e, HTTPException): raise e
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
            raise HTTPException(status_code=404, detail="Curso não encontrado")
        if existing.data[0]['institution_id'] != current_user.id:
             raise HTTPException(status_code=403, detail="Sem permissão para deletar este curso")
    except Exception as e:
         if isinstance(e, HTTPException): raise e
         raise HTTPException(status_code=500, detail=str(e))
    
    try:
        supabase.table("courses").delete().eq("id", str(course_id)).execute()
        return {"message": "Curso deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))