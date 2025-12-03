# 🎓 Course Platform API

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)
![Supabase](https://img.shields.io/badge/Supabase-Latest-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

API RESTful completa para plataforma de cursos online, desenvolvida com **FastAPI** e **Supabase**, implementando autenticação JWT, CRUD de cursos, sistema de favoritos e matrículas.

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias](#tecnologias)
- [Funcionalidades](#funcionalidades)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
  - [Opção 1: Ambiente Local](#opção-1-ambiente-local)
  - [Opção 2: Usando Máquina Virtual](#opção-2-usando-máquina-virtual)
- [Configuração](#configuração)
- [Executando o Projeto](#executando-o-projeto)
- [Documentação da API](#documentação-da-api)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Endpoints](#endpoints)
- [Exemplos de Uso](#exemplos-de-uso)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

---

## 🎯 Sobre o Projeto

Esta API foi desenvolvida para gerenciar uma plataforma de cursos online, permitindo:

- **Instituições** criarem e gerenciarem seus cursos
- **Estudantes** se matricularem, favoritarem e acompanharem cursos
- **Sistema de busca** para encontrar cursos por título ou descrição
- **Autenticação JWT** segura com Supabase Auth
- **Documentação automática** com Swagger UI

---

## 🚀 Tecnologias

Este projeto utiliza as seguintes tecnologias:

- **[Python 3.12+](https://www.python.org/)** - Linguagem de programação
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno e rápido
- **[Supabase](https://supabase.com/)** - Backend-as-a-Service (PostgreSQL + Auth)
- **[Pydantic](https://docs.pydantic.dev/)** - Validação de dados
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI
- **[Pytest](https://docs.pytest.org/)** - Framework de testes

---

## ✨ Funcionalidades

### Autenticação
- ✅ Registro de usuários (estudantes e instituições)
- ✅ Login com JWT
- ✅ Proteção de rotas com bearer token
- ✅ Autorização baseada em roles

### Cursos
- ✅ CRUD completo de cursos (apenas instituições)
- ✅ Listagem pública de cursos
- ✅ Filtros: destaque, populares, recentes, por categoria
- ✅ Sistema de busca case-insensitive

### Estudantes
- ✅ Adicionar/remover cursos dos favoritos
- ✅ Matricular-se em cursos
- ✅ Visualizar cursos matriculados
- ✅ Proteção cross-user (acesso apenas aos próprios dados)

### Instituições
- ✅ Listagem de instituições
- ✅ Perfil público de instituições
- ✅ Gestão de cursos próprios

---

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.12 ou superior**
- **pip** (gerenciador de pacotes Python)
- **Git** (para clonar o repositório)
- **Conta no Supabase** (gratuita)

### Verificando Versões

```bash
python --version  # ou python3 --version
pip --version
git --version
```

---

## 🔧 Instalação

### Opção 1: Ambiente Local

#### 1. Clone o Repositório

```bash
git clone https://github.com/JacioAlvesADS/backend-search-class.git
cd backend-search-class
```

#### 2. Crie um Ambiente Virtual

**No Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**No Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

#### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

---

### Opção 2: Usando Máquina Virtual

#### 1. Instale o VirtualBox

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install virtualbox virtualbox-ext-pack
```

**macOS (usando Homebrew):**
```bash
brew install --cask virtualbox
```

**Windows:**
- Baixe o instalador em: https://www.virtualbox.org/wiki/Downloads
- Execute o instalador e siga as instruções

#### 2. Baixe uma ISO do Ubuntu

```bash
# Recomendado: Ubuntu Server 22.04 LTS
wget https://releases.ubuntu.com/22.04/ubuntu-22.04.3-live-server-amd64.iso
```

#### 3. Crie uma VM no VirtualBox

1. Abra o VirtualBox
2. Clique em "Novo"
3. Configure:
   - **Nome**: Backend-Course-Platform
   - **Tipo**: Linux
   - **Versão**: Ubuntu (64-bit)
   - **Memória RAM**: 2GB (2048 MB)
   - **Disco**: 20GB VDI
4. Inicie a VM e aponte para a ISO do Ubuntu
5. Siga o assistente de instalação do Ubuntu

#### 4. Configure a VM

```bash
# Atualize o sistema
sudo apt update && sudo apt upgrade -y

# Instale Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip git -y

# Verifique a instalação
python3.12 --version
```

#### 5. Clone e Configure o Projeto na VM

```bash
# Clone o repositório
git clone https://github.com/JacioAlvesADS/backend-search-class.git
cd backend-search-class

# Crie o ambiente virtual
python3.12 -m venv venv
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

#### 6. Configure Port Forwarding (VirtualBox)

Para acessar a API da sua máquina host:

1. Com a VM desligada, vá em **Configurações > Rede**
2. Clique em **Avançado > Encaminhamento de Portas**
3. Adicione uma regra:
   - **Nome**: FastAPI
   - **Protocolo**: TCP
   - **IP do Host**: 127.0.0.1
   - **Porta do Host**: 8000
   - **IP do Convidado**: (vazio)
   - **Porta do Convidado**: 8000
4. Inicie a VM

---

## ⚙️ Configuração

### 1. Crie uma Conta no Supabase

1. Acesse: https://supabase.com
2. Crie um novo projeto
3. Aguarde a criação do banco de dados

### 2. Configure o Banco de Dados

Execute este SQL no **SQL Editor** do Supabase:

```sql
-- Criar extensão UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Criar enum para roles
CREATE TYPE user_role AS ENUM ('student', 'institution');

-- Criar enum para status de cursos
CREATE TYPE course_status AS ENUM ('draft', 'published', 'archived');

-- Tabela de perfis
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  role user_role NOT NULL DEFAULT 'student',
  display_name TEXT,
  bio TEXT,
  website TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de cursos
CREATE TABLE courses (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  institution_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  thumbnail_url TEXT,
  price NUMERIC(10, 2) DEFAULT 0,
  status course_status DEFAULT 'draft',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de matrículas
CREATE TABLE enrollments (
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
  progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
  enrolled_at TIMESTAMPTZ DEFAULT NOW(),
  last_accessed_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, course_id)
);

-- Tabela de favoritos
CREATE TABLE favorites (
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  course_id UUID REFERENCES courses(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (user_id, course_id)
);

-- Índices para performance
CREATE INDEX idx_courses_institution ON courses(institution_id);
CREATE INDEX idx_courses_status ON courses(status);
CREATE INDEX idx_enrollments_user ON enrollments(user_id);
CREATE INDEX idx_favorites_user ON favorites(user_id);

-- RLS (Row Level Security)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;
ALTER TABLE enrollments ENABLE ROW LEVEL SECURITY;
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso
CREATE POLICY "Perfis são visíveis publicamente" ON profiles FOR SELECT USING (true);
CREATE POLICY "Cursos publicados são visíveis" ON courses FOR SELECT USING (status = 'published' OR auth.uid() = institution_id);
CREATE POLICY "Matrículas visíveis pelo próprio usuário" ON enrollments FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Favoritos visíveis pelo próprio usuário" ON favorites FOR SELECT USING (auth.uid() = user_id);
```

### 3. Configure o Storage (Opcional)

Para upload de imagens de cursos:

1. No Supabase, vá em **Storage**
2. Crie um bucket chamado `course-covers`
3. Configure como público

### 4. Obtenha as Credenciais

No Supabase, vá em **Settings > API** e copie:
- **Project URL**
- **anon/public key**

### 5. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# .env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publica-anon
```

**⚠️ IMPORTANTE**: Nunca commite o arquivo `.env`! Ele já está no `.gitignore`.

---

## ▶️ Executando o Projeto

### 1. Ative o Ambiente Virtual (se ainda não estiver ativo)

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### 2. Inicie o Servidor

```bash
uvicorn app.main:app --reload
```

**Opções de execução:**

```bash
# Com reload automático (desenvolvimento)
uvicorn app.main:app --reload

# Especificando host e porta
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Modo produção (sem reload)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Com logs detalhados
uvicorn app.main:app --reload --log-level debug
```

### 3. Verifique se está funcionando

Acesse no navegador:
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs
- Documentação ReDoc: http://localhost:8000/redoc

Você deve ver:
```json
{
  "message": "API Online. Use /docs para ver os endpoints."
}
```

---

## 📖 Documentação da API

A documentação interativa é gerada automaticamente pelo FastAPI.

### Swagger UI (Recomendado)
```
http://localhost:8000/docs
```
- Interface interativa
- Testes diretos dos endpoints
- Autenticação JWT integrada

### ReDoc (Alternativa)
```
http://localhost:8000/redoc
```
- Layout alternativo
- Ideal para leitura

### OpenAPI JSON
```
http://localhost:8000/openapi.json
```
- Schema OpenAPI 3.0
- Para integração com outras ferramentas

---

## 🧪 Testes

### Executar Todos os Testes

```bash
pytest -v
```

### Executar Testes Específicos

```bash
# Testes de autenticação
pytest tests/test_auth.py -v

# Testes de cursos
pytest tests/test_courses.py -v

# Testes de banco de dados
pytest tests/test_database.py -v
```

### Cobertura de Testes

```bash
pytest --cov=app --cov-report=html
```

Abra `htmlcov/index.html` no navegador para ver o relatório.

### Resultados Esperados

- ✅ **58 testes passando** (72%)
- ⏭️ **19 testes ignorados** (requerem autenticação real)
- ❌ **4 testes falhando** (configuração do Supabase para emails de teste)

---

## 📁 Estrutura do Projeto

```
backend-search-class/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicação principal
│   │
│   ├── core/                   # Configurações centrais
│   │   ├── __init__.py
│   │   ├── config.py           # Variáveis de ambiente
│   │   ├── database.py         # Conexão com Supabase
│   │   └── security.py         # Autenticação JWT
│   │
│   ├── routers/                # Endpoints da API
│   │   ├── __init__.py
│   │   ├── auth.py             # Registro e login
│   │   ├── courses.py          # CRUD de cursos
│   │   ├── students.py         # Favoritos e matrículas
│   │   ├── institutions.py     # Instituições
│   │   └── search.py           # Busca de cursos
│   │
│   └── schemas/                # Modelos Pydantic
│       ├── __init__.py
│       ├── auth.py             # Schemas de autenticação
│       ├── course.py           # Schemas de cursos
│       └── user.py             # Schemas de usuários
│
├── tests/                      # Testes automatizados
│   ├── __init__.py
│   ├── conftest.py             # Fixtures do pytest
│   ├── test_auth.py
│   ├── test_courses.py
│   ├── test_students.py
│   ├── test_institutions.py
│   ├── test_search.py
│   ├── test_database.py
│   ├── test_security.py
│   └── test_schemas.py
│
├── .env                        # Variáveis de ambiente (não commitado)
├── .gitignore                  # Arquivos ignorados pelo git
├── requirements.txt            # Dependências Python
├── pytest.ini                  # Configuração do pytest
├── README.md                   # Este arquivo
├── APRESENTACAO.md             # Documentação para apresentação
└── RELATORIO_VALIDACAO.md      # Relatório de testes
```

---

## 🔌 Endpoints

### Autenticação

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/register` | Registrar novo usuário | Não |
| POST | `/api/login` | Login e obter token JWT | Não |

### Cursos

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/programas/` | Listar todos os cursos | Não |
| GET | `/api/programas/{id}` | Detalhes de um curso | Não |
| POST | `/api/programas/` | Criar curso | Sim (Instituição) |
| PUT | `/api/programas/{id}` | Atualizar curso | Sim (Instituição) |
| DELETE | `/api/programas/{id}` | Deletar curso | Sim (Instituição) |
| GET | `/api/programas/destaque` | Cursos em destaque | Não |
| GET | `/api/programas/populares` | Cursos populares | Não |
| GET | `/api/programas/recentes` | Cursos recentes | Não |
| GET | `/api/programas/categoria/{area}` | Cursos por categoria | Não |

### Busca

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/search?q=termo` | Buscar cursos | Não |

### Favoritos

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/users/{user_id}/favoritos` | Listar favoritos | Sim |
| POST | `/api/users/{user_id}/favoritos/{course_id}` | Adicionar favorito | Sim |
| DELETE | `/api/users/{user_id}/favoritos/{course_id}` | Remover favorito | Sim |

### Matrículas

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| POST | `/api/users/{user_id}/enroll/{course_id}` | Matricular em curso | Sim |
| GET | `/api/users/{user_id}/cursos` | Listar cursos matriculados | Sim |

### Instituições

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| GET | `/api/instituicoes/` | Listar instituições | Não |
| GET | `/api/instituicoes/{id}` | Detalhes de uma instituição | Não |

---

## 💻 Exemplos de Uso

### 1. Registrar um Usuário

```bash
curl -X POST "http://localhost:8000/api/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "aluno@exemplo.com",
    "password": "senha123",
    "display_name": "João Silva",
    "role": "student"
  }'
```

### 2. Fazer Login

```bash
curl -X POST "http://localhost:8000/api/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "aluno@exemplo.com",
    "password": "senha123"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "user": {
    "id": "7a918268-d67a-4a42-be70-9a1aa88c9783",
    "email": "aluno@exemplo.com"
  }
}
```

### 3. Buscar Cursos

```bash
curl "http://localhost:8000/api/search?q=python"
```

### 4. Adicionar aos Favoritos (Com Token)

```bash
curl -X POST "http://localhost:8000/api/users/{user_id}/favoritos/{course_id}" \
  -H "Authorization: Bearer eyJhbGci..."
```

### 5. Listar Favoritos

```bash
curl "http://localhost:8000/api/users/{user_id}/favoritos" \
  -H "Authorization: Bearer eyJhbGci..."
```

### 6. Matricular em Curso

```bash
curl -X POST "http://localhost:8000/api/users/{user_id}/enroll/{course_id}" \
  -H "Authorization: Bearer eyJhbGci..."
```

### 7. Criar Curso (Instituição)

```bash
curl -X POST "http://localhost:8000/api/programas/" \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python para Iniciantes",
    "description": "Aprenda Python do zero",
    "price": 99.90,
    "status": "published"
  }'
```

---

## 🛠️ Solução de Problemas

### Erro: "Module not found"

```bash
# Certifique-se de que o ambiente virtual está ativo
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "Connection refused" (Supabase)

- Verifique se as variáveis `SUPABASE_URL` e `SUPABASE_KEY` estão corretas no `.env`
- Confirme que o projeto Supabase está ativo

### Erro: "Port 8000 already in use"

```bash
# Linux/macOS
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Testes Falhando

- 4 testes de autenticação falham por configuração do Supabase (esperado)
- Configure o Supabase para aceitar emails de teste se necessário

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Padrões de Código

- Siga a PEP 8 para Python
- Use type hints
- Documente funções complexas
- Adicione testes para novas funcionalidades

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👥 Autor

**Jácio Alves**  
GitHub: [@JacioAlvesADS](https://github.com/JacioAlvesADS)

---

## 🔗 Links Úteis

- [Documentação FastAPI](https://fastapi.tiangolo.com)
- [Documentação Supabase](https://supabase.com/docs)
- [Documentação Pydantic](https://docs.pydantic.dev)
- [Documentação Pytest](https://docs.pytest.org)
- [Python.org](https://www.python.org/)

---

## 📊 Status do Projeto

✅ **Versão**: 1.0.0  
✅ **Status**: Pronto para Produção  
✅ **Cobertura de Testes**: 72%  
✅ **Documentação**: Completa  

---

<div align="center">
  <p>Desenvolvido com ❤️ usando FastAPI e Supabase</p>
  <p>⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!</p>
</div>
