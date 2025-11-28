import pytest
from fastapi import status

class TestAuthentication:
    """Testes para autenticação de usuários"""
    
    def test_root_endpoint(self, client):
        """Testa se a API está online"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "API Online" in response.json()["message"]
    
    def test_register_student_success(self, client, test_user_student):
        """Testa registro de estudante com sucesso"""
        response = client.post("/api/register", json=test_user_student)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "message" in data
        assert "sucesso" in data["message"].lower()
    
    def test_register_institution_success(self, client, test_user_institution):
        """Testa registro de instituição com sucesso"""
        response = client.post("/api/register", json=test_user_institution)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "message" in data
        assert "sucesso" in data["message"].lower()
    
    def test_register_invalid_email(self, client):
        """Testa registro com e-mail inválido"""
        invalid_user = {
            "email": "invalid-email",
            "password": "Test123456",
            "display_name": "Test User",
            "role": "student"
        }
        response = client.post("/api/register", json=invalid_user)
        assert response.status_code == 422  # Validation error
    
    def test_register_short_password(self, client):
        """Testa registro com senha muito curta"""
        invalid_user = {
            "email": "test@test.com",
            "password": "123",
            "display_name": "Test User",
            "role": "student"
        }
        response = client.post("/api/register", json=invalid_user)
        assert response.status_code == 422  # Validation error
    
    def test_register_duplicate_email(self, client, test_user_student):
        """Testa registro com e-mail duplicado"""
        # Primeiro registro
        client.post("/api/register", json=test_user_student)
        
        # Tentativa de registro duplicado
        response = client.post("/api/register", json=test_user_student)
        assert response.status_code == 400
    
    def test_login_success(self, client, test_user_student):
        """Testa login com credenciais válidas"""
        # Registrar primeiro
        client.post("/api/register", json=test_user_student)
        
        # Login
        login_data = {
            "email": test_user_student["email"],
            "password": test_user_student["password"]
        }
        response = client.post("/api/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user_student["email"]
    
    def test_login_invalid_credentials(self, client):
        """Testa login com credenciais inválidas"""
        login_data = {
            "email": "nonexistent@test.com",
            "password": "WrongPassword123"
        }
        response = client.post("/api/login", json=login_data)
        assert response.status_code == 400
    
    def test_login_wrong_password(self, client, test_user_student):
        """Testa login com senha incorreta"""
        # Registrar primeiro
        client.post("/api/register", json=test_user_student)
        
        # Tentar login com senha errada
        login_data = {
            "email": test_user_student["email"],
            "password": "WrongPassword123"
        }
        response = client.post("/api/login", json=login_data)
        assert response.status_code == 400
    
    def test_token_structure(self, client, test_user_student):
        """Testa estrutura do token JWT"""
        # Registrar e fazer login
        client.post("/api/register", json=test_user_student)
        
        login_data = {
            "email": test_user_student["email"],
            "password": test_user_student["password"]
        }
        response = client.post("/api/login", json=login_data)
        
        data = response.json()
        token = data["access_token"]
        
        # Token JWT deve ter 3 partes separadas por pontos
        assert token.count('.') >= 2
        assert len(token) > 50  # Token deve ter tamanho mínimo
