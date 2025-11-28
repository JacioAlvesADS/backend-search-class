import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import supabase
from uuid import uuid4
import os

@pytest.fixture
def client():
    """Cliente de teste para a API"""
    return TestClient(app)

@pytest.fixture
def test_user_student():
    """Dados de usuário estudante para testes"""
    return {
        "email": f"student_{uuid4()}@test.com",
        "password": "Test123456",
        "display_name": "Test Student",
        "role": "student"
    }

@pytest.fixture
def test_user_institution():
    """Dados de usuário instituição para testes"""
    return {
        "email": f"institution_{uuid4()}@test.com",
        "password": "Test123456",
        "display_name": "Test Institution",
        "role": "institution"
    }

@pytest.fixture
def test_course_data():
    """Dados de curso para testes"""
    return {
        "title": "Curso de Python Avançado",
        "description": "Aprenda Python do zero ao avançado com projetos práticos",
        "price": 199.90,
        "status": "published"
    }

@pytest.fixture
def authenticated_student(client, test_user_student):
    """Cria e autentica um estudante para testes"""
    # Registrar
    register_response = client.post("/api/register", json=test_user_student)
    
    # Login
    login_response = client.post("/api/login", json={
        "email": test_user_student["email"],
        "password": test_user_student["password"]
    })
    
    token_data = login_response.json()
    user_id = token_data["user"]["id"]
    
    return {
        "token": token_data["access_token"],
        "user_id": user_id,
        "email": test_user_student["email"]
    }

@pytest.fixture
def authenticated_institution(client, test_user_institution):
    """Cria e autentica uma instituição para testes"""
    # Registrar
    register_response = client.post("/api/register", json=test_user_institution)
    
    # Login
    login_response = client.post("/api/login", json={
        "email": test_user_institution["email"],
        "password": test_user_institution["password"]
    })
    
    token_data = login_response.json()
    user_id = token_data["user"]["id"]
    
    return {
        "token": token_data["access_token"],
        "user_id": user_id,
        "email": test_user_institution["email"]
    }

@pytest.fixture
def cleanup_test_data():
    """Fixture para limpar dados de teste após os testes"""
    test_emails = []
    test_course_ids = []
    
    yield {
        "emails": test_emails,
        "course_ids": test_course_ids
    }
    
    # Cleanup após os testes
    for email in test_emails:
        try:
            # Buscar usuário
            user = supabase.table("profiles").select("id").eq("email", email).execute()
            if user.data:
                user_id = user.data[0]["id"]
                # Deletar enrollments
                supabase.table("enrollments").delete().eq("user_id", user_id).execute()
                # Deletar favorites
                supabase.table("favorites").delete().eq("user_id", user_id).execute()
                # Deletar profile
                supabase.table("profiles").delete().eq("id", user_id).execute()
        except Exception as e:
            print(f"Erro ao limpar usuário {email}: {e}")
    
    for course_id in test_course_ids:
        try:
            supabase.table("enrollments").delete().eq("course_id", course_id).execute()
            supabase.table("favorites").delete().eq("course_id", course_id).execute()
            supabase.table("courses").delete().eq("id", course_id).execute()
        except Exception as e:
            print(f"Erro ao limpar curso {course_id}: {e}")
