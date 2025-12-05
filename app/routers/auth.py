from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from app.core.database import supabase

router = APIRouter(prefix="/auth", tags=["Autenticação"])

class LoginSchema(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(data: LoginSchema):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": data.email, 
            "password": data.password
        })
        
        if not response.user:
            raise HTTPException(status_code=400, detail="Login falhou")

        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "user_metadata": response.user.user_metadata
            }
        }
        
    except Exception as e:
        print(f"Erro no login: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="E-mail ou senha incorretos."
        )