from fastapi import APIRouter, HTTPException, status
from app.core.database import supabase
from app.schemas.auth import UserSignup, UserLogin, Token

router = APIRouter(tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserSignup):
    try:
        auth_response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password,
            "options": {
                "data": {
                    "display_name": user.display_name,
                    "role": user.role
                }
            }
        })
        
        if not auth_response.user:
            raise HTTPException(status_code=400, detail="Falha no cadastro.")

        try:
            supabase.table("profiles").insert({
                "id": str(auth_response.user.id),
                "role": user.role,
                "display_name": user.display_name,
            }).execute()
        except Exception as profile_e:
            supabase.auth.admin.delete_user(auth_response.user.id)
            raise HTTPException(status_code=500, detail=f"Erro ao criar perfil. Cadastro desfeito: {str(profile_e)}")


        return {"message": "Usuário criado com sucesso. Verifique seu e-mail para confirmar."}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        
        if not auth_response.session:
             raise HTTPException(status_code=401, detail="Credenciais inválidas")

        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer",
            "user": auth_response.user.model_dump()
        }
    except Exception as e:
          raise HTTPException(status_code=400, detail=str(e))