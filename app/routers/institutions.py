from fastapi import APIRouter, HTTPException
from app.core.database import supabase

router = APIRouter(prefix="/institutions", tags=["Instituições"])

@router.get("/")
async def list_institutions():
    try:
        response = supabase.table("profiles").select("*").eq("role", "institution").execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar instituições: {e}")
        return []