from fastapi import APIRouter, HTTPException
from typing import List, Optional
from uuid import UUID
from app.core.database import supabase
from app.schemas.user import InstitutionResponse 

router = APIRouter(prefix="/instituicoes", tags=["Institutions"])


@router.get("/", response_model=List[InstitutionResponse])
async def list_institutions():
    try:
        res = supabase.table("profiles").select("*").eq("role", "institution").execute()
        
        if not res.data:
            return []
            
        return res.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar instituições: {str(e)}")

@router.get("/{institution_id}", response_model=InstitutionResponse)
async def get_institution(institution_id: UUID):
    try:
        res = supabase.table("profiles").select("*").eq("id", str(institution_id)).eq("role", "institution").execute()
        
        if not res.data:
            raise HTTPException(status_code=404, detail="Instituição não encontrada")
            
        return res.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar instituição: {str(e)}")