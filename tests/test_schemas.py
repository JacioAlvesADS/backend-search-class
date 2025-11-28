import pytest
from pydantic import ValidationError
from app.schemas.auth import UserSignup, UserLogin, Token
from app.schemas.course import (
    CourseCreate, CourseUpdate, CourseResponse,
    CourseStatus, UserRole, ProfileResponse, EnrollmentResponse
)

class TestSchemas:
    """Testes para validar schemas Pydantic"""
    
    def test_user_signup_valid(self):
        """Testa criação de UserSignup válido"""
        data = {
            "email": "test@example.com",
            "password": "Test123456",
            "display_name": "Test User",
            "role": "student"
        }
        user = UserSignup(**data)
        assert user.email == "test@example.com"
        assert user.password == "Test123456"
        assert user.display_name == "Test User"
        assert user.role == UserRole.student
    
    def test_user_signup_invalid_email(self):
        """Testa que e-mail inválido gera erro"""
        data = {
            "email": "invalid-email",
            "password": "Test123456",
            "display_name": "Test User",
            "role": "student"
        }
        with pytest.raises(ValidationError):
            UserSignup(**data)
    
    def test_user_signup_short_password(self):
        """Testa que senha muito curta gera erro"""
        data = {
            "email": "test@example.com",
            "password": "123",
            "display_name": "Test User",
            "role": "student"
        }
        with pytest.raises(ValidationError):
            UserSignup(**data)
    
    def test_user_signup_default_role(self):
        """Testa que role padrão é student"""
        data = {
            "email": "test@example.com",
            "password": "Test123456",
            "display_name": "Test User"
        }
        user = UserSignup(**data)
        assert user.role == UserRole.student
    
    def test_user_login_valid(self):
        """Testa criação de UserLogin válido"""
        data = {
            "email": "test@example.com",
            "password": "Test123456"
        }
        login = UserLogin(**data)
        assert login.email == "test@example.com"
        assert login.password == "Test123456"
    
    def test_course_create_valid(self):
        """Testa criação de CourseCreate válido"""
        data = {
            "title": "Python Course",
            "description": "Learn Python",
            "price": 99.90,
            "status": "draft"
        }
        course = CourseCreate(**data)
        assert course.title == "Python Course"
        assert course.description == "Learn Python"
        assert course.price == 99.90
        assert course.status == CourseStatus.draft
    
    def test_course_create_default_status(self):
        """Testa que status padrão é draft"""
        data = {
            "title": "Python Course",
            "description": "Learn Python",
            "price": 99.90
        }
        course = CourseCreate(**data)
        assert course.status == CourseStatus.draft
    
    def test_course_update_partial(self):
        """Testa que CourseUpdate aceita campos opcionais"""
        data = {"title": "New Title"}
        update = CourseUpdate(**data)
        assert update.title == "New Title"
        assert update.description is None
        assert update.price is None
    
    def test_course_status_enum(self):
        """Testa valores válidos do enum CourseStatus"""
        assert CourseStatus.draft == "draft"
        assert CourseStatus.published == "published"
        assert CourseStatus.archived == "archived"
    
    def test_user_role_enum(self):
        """Testa valores válidos do enum UserRole"""
        assert UserRole.student == "student"
        assert UserRole.institution == "institution"
    
    def test_token_structure(self):
        """Testa estrutura do schema Token"""
        data = {
            "access_token": "fake_token_here",
            "token_type": "bearer",
            "user": {"id": "123", "email": "test@test.com"}
        }
        token = Token(**data)
        assert token.access_token == "fake_token_here"
        assert token.token_type == "bearer"
        assert token.user["email"] == "test@test.com"
    
    def test_profile_response_structure(self):
        """Testa estrutura do schema ProfileResponse"""
        from uuid import uuid4
        data = {
            "id": str(uuid4()),
            "email": "test@test.com",
            "role": "student",
            "display_name": "Test User"
        }
        profile = ProfileResponse(**data)
        assert profile.email == "test@test.com"
        assert profile.role == UserRole.student
    
    def test_enrollment_response_structure(self):
        """Testa estrutura do schema EnrollmentResponse"""
        from uuid import uuid4
        data = {
            "user_id": str(uuid4()),
            "course_id": str(uuid4()),
            "progress": 50
        }
        enrollment = EnrollmentResponse(**data)
        assert enrollment.progress == 50
    
    def test_enrollment_default_progress(self):
        """Testa que progress padrão é 0"""
        from uuid import uuid4
        data = {
            "user_id": str(uuid4()),
            "course_id": str(uuid4())
        }
        enrollment = EnrollmentResponse(**data)
        assert enrollment.progress == 0
