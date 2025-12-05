# Configuração do Banco de Dados (Supabase/PostgreSQL)

Este projeto utiliza **PostgreSQL** hospedado na plataforma **Supabase**.

## 1. Estrutura do Banco de Dados

Para rodar este projeto, execute o seguinte script SQL no **SQL Editor** do seu painel do Supabase para criar as tabelas e relacionamentos necessários.

```sql
-- 1. Criação da Tabela de Perfis (Vinculada ao Auth do Supabase)
create table public.profiles (
  id uuid references auth.users not null primary key,
  email text,
  display_name text,
  role text default 'student' check (role in ('student', 'institution')),
  bio text,
  website text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 2. Criação da Tabela de Cursos
create table public.courses (
  id uuid default gen_random_uuid() primary key,
  institution_id uuid references public.profiles(id) not null,
  title text not null,
  description text,
  price numeric default 0,
  status text default 'draft' check (status in ('draft', 'published', 'archived')),
  thumbnail_url text,
  category text, -- Campo para filtros de área
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- 3. Trigger para criar perfil automaticamente ao cadastrar usuário
-- (Opcional, mas recomendado para o Auth funcionar com a tabela profiles)
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email, display_name, role)
  values (new.id, new.email, new.raw_user_meta_data->>'display_name', 'student');
  return new;
end;
$$ language plpgsql security definer;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();
```

## 2. Configuração de Storage (Imagens)

O projeto requer um bucket de armazenamento para as capas dos cursos.

1.  No painel do Supabase, vá em **Storage**.
2.  Crie um novo bucket chamado: `course-covers`.
3.  Defina o bucket como **Public**.

## 3. Variáveis de Ambiente

O arquivo `.env` no backend deve conter as credenciais do projeto:

```env
SUPABASE_URL=https://seu-projeto-id.supabase.co
SUPABASE_KEY=sua-chave-anon-publica
SECRET_KEY=sua-chave-secreta-para-jwt
```