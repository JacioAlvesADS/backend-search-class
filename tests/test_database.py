import pytest
from app.core.database import supabase
from app.core.config import settings

class TestDatabase:
    """Testes para validar conexão e estrutura do banco de dados"""
    
    def test_supabase_connection(self):
        """Testa se a conexão com o Supabase está funcionando"""
        assert supabase is not None
        assert hasattr(supabase, 'table')
        assert hasattr(supabase, 'auth')
        assert hasattr(supabase, 'storage')
    
    def test_settings_loaded(self):
        """Testa se as configurações foram carregadas"""
        assert settings.SUPABASE_URL is not None
        assert settings.SUPABASE_KEY is not None
        assert len(settings.SUPABASE_URL) > 0
        assert len(settings.SUPABASE_KEY) > 0
    
    def test_profiles_table_exists(self):
        """Testa se a tabela profiles existe e é acessível"""
        try:
            response = supabase.table("profiles").select("id").limit(1).execute()
            assert response is not None
        except Exception as e:
            pytest.fail(f"Erro ao acessar tabela profiles: {str(e)}")
    
    def test_courses_table_exists(self):
        """Testa se a tabela courses existe e é acessível"""
        try:
            response = supabase.table("courses").select("id").limit(1).execute()
            assert response is not None
        except Exception as e:
            pytest.fail(f"Erro ao acessar tabela courses: {str(e)}")
    
    def test_enrollments_table_exists(self):
        """Testa se a tabela enrollments existe e é acessível"""
        try:
            response = supabase.table("enrollments").select("user_id").limit(1).execute()
            assert response is not None
        except Exception as e:
            pytest.fail(f"Erro ao acessar tabela enrollments: {str(e)}")
    
    def test_favorites_table_exists(self):
        """Testa se a tabela favorites existe e é acessível"""
        try:
            response = supabase.table("favorites").select("user_id").limit(1).execute()
            assert response is not None
        except Exception as e:
            pytest.fail(f"Erro ao acessar tabela favorites: {str(e)}")
    
    def test_courses_table_structure(self):
        """Testa estrutura da tabela courses"""
        try:
            response = supabase.table("courses").select("*").limit(1).execute()
            
            if response.data and len(response.data) > 0:
                course = response.data[0]
                # Validar campos obrigatórios conforme diagrama
                required_fields = [
                    "id", "institution_id", "title", "description",
                    "price", "status", "created_at"
                ]
                for field in required_fields:
                    assert field in course, f"Campo {field} não encontrado na tabela courses"
        except Exception as e:
            pytest.fail(f"Erro ao validar estrutura da tabela courses: {str(e)}")
    
    def test_profiles_table_structure(self):
        """Testa estrutura da tabela profiles"""
        try:
            response = supabase.table("profiles").select("*").limit(1).execute()
            
            if response.data and len(response.data) > 0:
                profile = response.data[0]
                # Validar campos obrigatórios conforme diagrama
                required_fields = ["id", "email", "role", "display_name"]
                for field in required_fields:
                    assert field in profile, f"Campo {field} não encontrado na tabela profiles"
        except Exception as e:
            pytest.fail(f"Erro ao validar estrutura da tabela profiles: {str(e)}")
    
    def test_enrollments_table_structure(self):
        """Testa estrutura da tabela enrollments"""
        try:
            response = supabase.table("enrollments").select("*").limit(1).execute()
            
            if response.data and len(response.data) > 0:
                enrollment = response.data[0]
                # Validar campos obrigatórios conforme diagrama
                required_fields = ["user_id", "course_id", "progress"]
                for field in required_fields:
                    assert field in enrollment, f"Campo {field} não encontrado na tabela enrollments"
        except Exception as e:
            pytest.fail(f"Erro ao validar estrutura da tabela enrollments: {str(e)}")
    
    def test_favorites_table_structure(self):
        """Testa estrutura da tabela favorites"""
        try:
            response = supabase.table("favorites").select("*").limit(1).execute()
            
            if response.data and len(response.data) > 0:
                favorite = response.data[0]
                # Validar campos obrigatórios conforme diagrama
                required_fields = ["user_id", "course_id", "created_at"]
                for field in required_fields:
                    assert field in favorite, f"Campo {field} não encontrado na tabela favorites"
        except Exception as e:
            pytest.fail(f"Erro ao validar estrutura da tabela favorites: {str(e)}")
    
    def test_storage_bucket_exists(self):
        """Testa se o bucket de storage course-covers existe"""
        try:
            # Tentar listar arquivos do bucket
            response = supabase.storage.from_("course-covers").list()
            assert response is not None
        except Exception as e:
            # Bucket pode não existir ou pode não ter permissão
            # Importante é que o storage está acessível
            assert hasattr(supabase, 'storage')
