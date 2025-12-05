from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import courses, auth, search, institutions, students

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router)
app.include_router(auth.router)
app.include_router(institutions.router)
# app.include_router(search.router)