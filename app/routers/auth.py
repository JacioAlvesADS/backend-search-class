from fastapi import APIRouter, HTTPException, status
from app.core.database import supabase
from app.schemas.auth import UserSignup, UserLogin, Token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
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
            raise HTTPException(status_code=400, detail="Signup failed")

        return {"message": "User created successfully. Please check your email to confirm."}

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
             raise HTTPException(status_code=401, detail="Invalid credentials")

        return {
            "access_token": auth_response.session.access_token,
            "token_type": "bearer",
            "user": auth_response.user.model_dump()
        }
    except Exception as e:
         raise HTTPException(status_code=400, detail=str(e))
