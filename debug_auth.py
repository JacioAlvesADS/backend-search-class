"""
Script de Debug - Autenticação Supabase
Testa diretamente as funções de auth para identificar o problema
"""

from app.core.database import supabase
from app.core.config import settings
import json
from uuid import uuid4

def test_connection():
    """Testa conexão com Supabase"""
    print("=" * 60)
    print("1. TESTANDO CONEXÃO COM SUPABASE")
    print("=" * 60)
    print(f"URL: {settings.SUPABASE_URL}")
    print(f"Key (primeiros 20 chars): {settings.SUPABASE_KEY[:20]}...")
    print("✅ Conexão estabelecida\n")

def test_sign_up():
    """Testa registro de novo usuário"""
    print("=" * 60)
    print("2. TESTANDO REGISTRO (SIGN UP)")
    print("=" * 60)
    
    test_email = f"debug_{uuid4()}@test.com"
    test_password = "Test123456"
    
    print(f"Email de teste: {test_email}")
    print(f"Password: {test_password}\n")
    
    try:
        response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password,
            "options": {
                "data": {
                    "display_name": "Debug User",
                    "role": "student"
                }
            }
        })
        
        print("✅ Sign up retornou resposta")
        print(f"Type: {type(response)}")
        print(f"Attributes: {dir(response)}\n")
        
        if hasattr(response, 'user') and response.user:
            print(f"✅ User criado: {response.user.id}")
            print(f"   Email: {response.user.email}")
            print(f"   User data: {json.dumps(response.user.user_metadata, indent=2)}\n")
            
            # Tentar inserir no profiles
            print("Tentando inserir no profiles...")
            try:
                profile_data = {
                    "id": str(response.user.id),
                    "email": test_email,
                    "role": "student",
                    "display_name": "Debug User"
                }
                profile_result = supabase.table("profiles").insert(profile_data).execute()
                print(f"✅ Profile criado: {profile_result.data}\n")
            except Exception as profile_error:
                print(f"❌ Erro ao criar profile: {str(profile_error)}\n")
        else:
            print("❌ User não foi criado")
            print(f"Response completa: {response}\n")
            
    except Exception as e:
        print(f"❌ ERRO no sign_up: {str(e)}")
        print(f"Tipo do erro: {type(e)}\n")

def test_sign_in():
    """Testa login com credenciais"""
    print("=" * 60)
    print("3. TESTANDO LOGIN (SIGN IN)")
    print("=" * 60)
    
    # Primeiro criar um usuário
    test_email = f"login_test_{uuid4()}@test.com"
    test_password = "Test123456"
    
    print(f"Criando usuário de teste: {test_email}\n")
    
    try:
        # Criar usuário
        signup_response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password
        })
        
        if not signup_response.user:
            print("❌ Não conseguiu criar usuário para teste de login\n")
            return
        
        print("✅ Usuário criado, tentando login...\n")
        
        # Tentar login
        login_response = supabase.auth.sign_in_with_password({
            "email": test_email,
            "password": test_password
        })
        
        print("✅ Login retornou resposta")
        print(f"Type: {type(login_response)}")
        print(f"Attributes: {dir(login_response)}\n")
        
        if hasattr(login_response, 'session') and login_response.session:
            print(f"✅ Session criada")
            print(f"   Access Token (primeiros 30): {login_response.session.access_token[:30]}...")
            print(f"   Token Type: {login_response.session.token_type}")
            print(f"   Expires in: {login_response.session.expires_in}s\n")
        else:
            print("❌ Session não foi criada\n")
        
        if hasattr(login_response, 'user') and login_response.user:
            print(f"✅ User no response")
            print(f"   ID: {login_response.user.id}")
            print(f"   Email: {login_response.user.email}\n")
        else:
            print("❌ User não está no response\n")
            
    except Exception as e:
        print(f"❌ ERRO no sign_in: {str(e)}")
        print(f"Tipo do erro: {type(e)}\n")

def test_table_access():
    """Testa acesso às tabelas"""
    print("=" * 60)
    print("4. TESTANDO ACESSO ÀS TABELAS")
    print("=" * 60)
    
    tables = ["profiles", "courses", "enrollments", "favorites"]
    
    for table in tables:
        try:
            result = supabase.table(table).select("*").limit(1).execute()
            print(f"✅ {table}: Acessível (rows: {len(result.data)})")
        except Exception as e:
            print(f"❌ {table}: Erro - {str(e)}")
    print()

def test_rls_policies():
    """Testa políticas RLS"""
    print("=" * 60)
    print("5. VERIFICANDO POLÍTICAS RLS")
    print("=" * 60)
    print("⚠️  Verificação manual necessária no painel do Supabase")
    print("   1. Acesse: Authentication > Policies")
    print("   2. Verifique políticas da tabela 'profiles'")
    print("   3. Deve permitir INSERT para usuários autenticados\n")

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SCRIPT DE DEBUG - AUTENTICAÇÃO SUPABASE")
    print("=" * 60 + "\n")
    
    test_connection()
    test_sign_up()
    test_sign_in()
    test_table_access()
    test_rls_policies()
    
    print("=" * 60)
    print("DEBUG COMPLETO")
    print("=" * 60)
    print("\nPróximos passos:")
    print("1. Analisar os erros acima")
    print("2. Verificar políticas RLS no painel do Supabase")
    print("3. Confirmar que email confirmation está desabilitado (para testes)")
    print("4. Ajustar código baseado nos resultados\n")
