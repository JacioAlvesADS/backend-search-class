# Suite de Testes - Backend Course Platform

## 📋 Visão Geral

Suite completa de testes para validar toda a aplicação FastAPI + Supabase.

## 🧪 Estrutura dos Testes

### 1. **test_auth.py** - Testes de Autenticação
- ✅ Registro de usuários (student e institution)
- ✅ Validação de e-mail e senha
- ✅ Login com credenciais válidas/inválidas
- ✅ Estrutura do token JWT
- ✅ Prevenção de registros duplicados

### 2. **test_courses.py** - Testes de Cursos
- ✅ Listagem de cursos (destaque, populares, recentes)
- ✅ Criação de cursos (apenas instituições)
- ✅ Atualização e exclusão de cursos
- ✅ Busca por categoria
- ✅ Validação de estrutura de resposta

### 3. **test_students.py** - Testes de Estudantes
- ✅ Gerenciamento de favoritos
- ✅ Matrícula em cursos
- ✅ Listagem de cursos matriculados
- ✅ Controle de acesso (usuário só acessa seus dados)

### 4. **test_institutions.py** - Testes de Instituições
- ✅ Listagem de instituições
- ✅ Busca de instituição por ID
- ✅ Validação de estrutura de resposta

### 5. **test_search.py** - Testes de Busca
- ✅ Busca com/sem query
- ✅ Busca case-insensitive
- ✅ Busca com caracteres especiais
- ✅ Validação de resultados

### 6. **test_database.py** - Testes de Banco de Dados
- ✅ Conexão com Supabase
- ✅ Existência das tabelas (profiles, courses, enrollments, favorites)
- ✅ Estrutura das tabelas conforme diagrama
- ✅ Validação de campos obrigatórios
- ✅ Acesso ao storage bucket

### 7. **test_security.py** - Testes de Segurança
- ✅ Proteção de endpoints
- ✅ Validação de tokens
- ✅ Controle de acesso baseado em roles
- ✅ Validação que senha não é exposta
- ✅ CORS configurado

### 8. **test_schemas.py** - Testes de Schemas
- ✅ Validação Pydantic
- ✅ Campos obrigatórios e opcionais
- ✅ Valores padrão
- ✅ Enums (UserRole, CourseStatus)

## 🚀 Como Executar os Testes

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Executar Todos os Testes

```bash
pytest
```

### Executar Testes Específicos

```bash
# Por arquivo
pytest tests/test_auth.py

# Por classe
pytest tests/test_auth.py::TestAuthentication

# Por função
pytest tests/test_auth.py::TestAuthentication::test_login_success

# Por categoria
pytest -m auth
pytest -m integration
```

### Executar com Mais Detalhes

```bash
# Verbose
pytest -v

# Com output de prints
pytest -s

# Com coverage
pytest --cov=app --cov-report=html
```

## 📊 Cobertura de Testes

Os testes cobrem:

- ✅ **Autenticação**: registro, login, tokens
- ✅ **Autorização**: controle de acesso, roles
- ✅ **CRUD**: operações em todas as entidades
- ✅ **Validação**: schemas, campos obrigatórios
- ✅ **Banco de Dados**: estrutura, conexão, tabelas
- ✅ **Segurança**: proteção de endpoints, exposição de dados
- ✅ **Busca**: funcionalidade de pesquisa
- ✅ **Relacionamentos**: favorites, enrollments

## ⚠️ Validações Importantes

### Estrutura do Banco (conforme diagrama)

**Tabela: profiles**
- ✅ id (uuid, PK)
- ✅ email (text)
- ✅ role (user_role enum)
- ✅ display_name (text)
- ✅ avatar_url (text, optional)
- ✅ bio (text, optional)
- ✅ website (text, optional)
- ✅ created_at (timestamptz)
- ✅ updated_at (timestamptz)

**Tabela: courses**
- ✅ id (uuid, PK)
- ✅ institution_id (uuid, FK → profiles.id)
- ✅ title (text)
- ✅ description (text)
- ✅ thumbnail_url (text, optional)
- ✅ price (numeric)
- ✅ status (course_status enum)
- ✅ created_at (timestamptz)
- ✅ updated_at (timestamptz)

**Tabela: enrollments**
- ✅ user_id (uuid, PK, FK → profiles.id)
- ✅ course_id (uuid, PK, FK → courses.id)
- ✅ progress (int4)
- ✅ enrolled_at (timestamptz)
- ✅ last_accessed_at (timestamptz)

**Tabela: favorites**
- ✅ user_id (uuid, PK, FK → profiles.id)
- ✅ course_id (uuid, PK, FK → courses.id)
- ✅ created_at (timestamptz)

### Regras de Negócio Validadas

1. ✅ Apenas instituições podem criar cursos
2. ✅ Usuário só pode acessar seus próprios dados
3. ✅ Usuário só pode editar/deletar seus próprios cursos
4. ✅ Senha deve ter no mínimo 6 caracteres
5. ✅ E-mail deve ser válido
6. ✅ Não pode haver e-mails duplicados
7. ✅ Favorites e enrollments têm chave composta (user_id, course_id)
8. ✅ Progress padrão é 0 em enrollments

## 🔧 Configuração

Os testes utilizam as mesmas variáveis de ambiente do `.env`:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

## 📝 Notas Importantes

1. **Dados de Teste**: Os testes criam dados temporários e tentam limpá-los ao final
2. **Conexão Real**: Os testes fazem conexões reais com Supabase
3. **Tokens JWT**: Tokens reais são gerados durante os testes
4. **Storage**: Alguns testes podem falhar se o bucket não estiver configurado

## 🎯 Próximos Passos

Para melhorar ainda mais:

1. Adicionar testes de performance
2. Implementar mocks para testes unitários puros
3. Adicionar testes de carga
4. Configurar CI/CD com GitHub Actions
5. Adicionar coverage reports

## ✅ Conclusão

Esta suite de testes valida **toda a aplicação** de acordo com:
- ✅ Estrutura das tabelas no Supabase (conforme diagrama)
- ✅ Regras de negócio
- ✅ Segurança e autenticação
- ✅ Validação de dados
- ✅ Controle de acesso
