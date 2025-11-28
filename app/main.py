from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth
from app.routers import courses
from app.routers import students
from app.routers import institutions
from app.routers import search
from app.core.config import settings

app = FastAPI(
    title="Course Platform API",
    description="Backend for a course platform using FastAPI and Supabase",
    version="1.0.0"
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:4200",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router)
api_router.include_router(courses.router)
api_router.include_router(students.router)
api_router.include_router(institutions.router)
api_router.include_router(search.router)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "API Online. Use /docs para ver os endpoints."}