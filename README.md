# 🟢 Leggal - Assistente Inteligente de Produtividade

> Sistema de gerenciamento de tarefas com IA que recebe pedidos via chat, organiza automaticamente e ajuda na priorização.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Início Rápido](#-início-rápido)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [API Documentation](#-api-documentation)
- [Desenvolvimento](#-desenvolvimento)
- [Testes](#-testes)
- [Deploy](#-deploy)
- [Documentação Adicional](#-documentação-adicional)

## 🎯 Visão Geral

Leggal é um assistente inteligente que combina IA conversacional com gerenciamento de tarefas. Através de um chat intuitivo (simulando WhatsApp), o sistema:

1. **Recebe pedidos em linguagem natural**
2. **Analisa e extrai informações** usando OpenAI
3. **Cria tarefas automaticamente** com título, descrição e prioridade
4. **Responde perguntas** sobre suas tarefas e agenda
5. **Prioriza inteligentemente** baseado em urgência e impacto

## ✨ Funcionalidades

### 🤖 IA Conversacional
- Chat inteligente que entende contexto
- Diferencia perguntas de ações
- Respostas empáticas e personalizadas
- Histórico de conversas persistente

### 📊 Gerenciamento de Tarefas
- Criação automática via chat
- Priorização inteligente (Baixa, Média, Alta, Urgente)
- Busca semântica
- Filtros por status (Ativas/Concluídas)
- Transições de estado (Iniciar, Concluir, Reabrir)

### 🔐 Segurança
- Autenticação JWT
- Senhas hasheadas (PBKDF2)
- CORS configurado
- Validação de dados com Pydantic

### 🎨 Interface Moderna
- Design responsivo
- Tema verde (WhatsApp) e branco
- Experiência mobile-friendly
- Feedback visual em tempo real

## 🏗️ Arquitetura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   React     │──────│   FastAPI   │──────│ PostgreSQL  │
│  Frontend   │ HTTP │   Backend   │ SQL  │  Database   │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            │ API
                            ▼
                     ┌─────────────┐
                     │   OpenAI    │
                     │     API     │
                     └─────────────┘
```

### Padrões de Arquitetura

- **Separation of Concerns**: Backend e Frontend separados
- **Repository Pattern**: Camada de acesso a dados isolada
- **Service Layer**: Lógica de negócios centralizada
- **DTO Pattern**: Schemas Pydantic para validação
- **Dependency Injection**: FastAPI dependencies

## 🛠️ Tecnologias

### Backend
| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| Python | 3.11+ | Linguagem principal |
| FastAPI | 0.104+ | Framework web assíncrono |
| SQLAlchemy | 2.0+ | ORM |
| Alembic | 1.12+ | Migrações |
| OpenAI | 1.3+ | IA conversacional |
| PostgreSQL | 15+ | Banco de dados |
| PyJWT | 2.8+ | Autenticação JWT |

### Frontend
| Tecnologia | Versão | Uso |
|-----------|--------|-----|
| React | 18+ | UI Framework |
| TypeScript | 5.0+ | Type Safety |
| Vite | 5.0+ | Build Tool |
| Tailwind CSS | 3.3+ | Styling |
| React Query | 4.0+ | State Management |
| Axios | 1.6+ | HTTP Client |

## 🚀 Início Rápido

### Pré-requisitos
- Docker & Docker Compose
- Node.js 18+ (para desenvolvimento frontend)
- Python 3.11+ (para desenvolvimento backend)
- Chave API OpenAI

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd test-leggal
```

### 2. Configure as Variáveis de Ambiente

Crie o arquivo `backend/.env`:
```env
# Database
DATABASE_URL=postgresql://leggal_user:leggal_password@postgres:5432/leggal_db

# JWT
SECRET_KEY=your-secret-key-here-make-it-long-and-random
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# OpenAI
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL_NAME=gpt-4o-mini

# Server
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### 3. Inicie com Docker Compose
```bash
# Subir todos os serviços
docker-compose up -d

# Acompanhar logs
docker-compose logs -f backend

# Parar serviços
docker-compose down
```

### 4. Acesse a Aplicação
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Credenciais de Teste
```
Email: teste@leggal.com
Senha: 123456
```

## 📁 Estrutura do Projeto

```
test-leggal/
├── backend/                    # Backend Python/FastAPI
│   ├── app/
│   │   ├── core/              # Configurações e segurança
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── security.py
│   │   │   └── dependencies.py
│   │   ├── models/            # Modelos SQLAlchemy
│   │   │   ├── models.py
│   │   │   └── schemas.py
│   │   ├── routers/           # Endpoints da API
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   ├── chat.py
│   │   │   ├── webhook.py
│   │   │   └── ai.py
│   │   ├── services/          # Lógica de negócios
│   │   │   ├── auth_service.py
│   │   │   ├── task_service.py
│   │   │   ├── ai_service.py
│   │   │   └── webhook_service.py
│   │   ├── utils/             # Utilitários
│   │   │   ├── helpers.py
│   │   │   └── seed.py
│   │   ├── constants.py       # Constantes globais
│   │   └── main.py           # Entry point
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # Frontend React/TypeScript
│   ├── src/
│   │   ├── components/        # Componentes reutilizáveis
│   │   │   ├── Header.tsx
│   │   │   └── Logo.tsx
│   │   ├── pages/             # Páginas da aplicação
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── ChatPage.tsx
│   │   │   ├── TasksPage.tsx
│   │   │   └── ProfilePage.tsx
│   │   ├── hooks/             # Custom Hooks
│   │   │   └── useAuth.ts
│   │   ├── services/          # API Services
│   │   │   └── api.ts
│   │   ├── constants/         # Constantes
│   │   │   └── priorities.ts
│   │   ├── utils/             # Utilitários
│   │   │   └── formatters.ts
│   │   ├── types/             # TypeScript types
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── docker-compose.yml
├── DECISIONS.md              # Decisões de arquitetura
├── TESTING.md                # Guia de testes
└── README.md
```

## 📚 API Documentation

### Autenticação

#### POST /auth/register
Criar nova conta de usuário.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "senha123",
  "name": "Nome do Usuário"
}
```

#### POST /auth/login
Autenticar usuário.

**Body (form-data):**
```
username: user@example.com
password: senha123
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

#### GET /auth/me
Obter perfil do usuário autenticado.

**Headers:** `Authorization: Bearer <token>`

### Tarefas

#### GET /tasks
Listar tarefas do usuário.

**Query Params:**
- `status`: PENDING | IN_PROGRESS | COMPLETED
- `priority`: LOW | MEDIUM | HIGH | URGENT
- `search`: texto de busca
- `limit`: limite de resultados (default: 50)
- `offset`: paginação

#### POST /tasks
Criar nova tarefa.

**Body:**
```json
{
  "title": "Comprar material",
  "description": "Comprar material de escritório",
  "priority": "MEDIUM",
  "status": "PENDING"
}
```

#### PUT /tasks/{id}
Atualizar tarefa.

#### DELETE /tasks/{id}
Deletar tarefa.

### Chat

#### POST /chat/message
Enviar mensagem para o assistente.

**Body:**
```json
{
  "message": "Preciso revisar contrato urgente"
}
```

**Response:**
```json
{
  "type": "task_created",
  "content": "✅ Tarefa criada com sucesso!...",
  "task": {
    "id": "uuid",
    "title": "Revisar contrato",
    "priority": "URGENT"
  }
}
```

#### GET /chat/history
Obter histórico de conversas.

## 🧪 Desenvolvimento

### Backend Local

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instalar dependências
pip install -r requirements.txt

# Criar tabelas do banco
PYTHONPATH=. python scripts/init.py

# Popular com dados de teste
PYTHONPATH=. python app/utils/seed.py

# Iniciar servidor
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Local

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar dev server
npm run dev

# Build para produção
npm run build

# Preview do build
npm run preview
```

### Padrões de Código

#### Backend
- **PEP 8** para estilo de código Python
- **Type hints** em todas as funções
- **Docstrings** para funções públicas
- **Constantes** em UPPER_CASE
- **Services** para lógica de negócios
- **Schemas** para validação de dados

#### Frontend
- **ESLint** + **Prettier** para formatação
- **TypeScript strict mode**
- **Component-per-file** pattern
- **Custom hooks** para lógica reutilizável
- **Constants** em arquivos separados
- **Utility functions** tipadas

## 🧪 Testes

### Backend
```bash
cd backend

# Executar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth.py -v
```

### Frontend
```bash
cd frontend

# Executar testes
npm test

# Com cobertura
npm test -- --coverage
```

## 🚀 Deploy

### Docker Production

```bash
# Build de produção
docker-compose -f docker-compose.prod.yml up -d

# Logs
docker-compose logs -f

# Backup do banco
docker exec postgres pg_dump -U leggal_user leggal_db > backup.sql
```

### Variáveis de Ambiente - Produção

```env
ENVIRONMENT=production
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=<secure-random-key>
OPENAI_API_KEY=<your-api-key>
ALLOWED_ORIGINS=https://yourdomain.com
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/MinhaFeature`
3. Commit: `git commit -m 'Add: nova feature'`
4. Push: `git push origin feature/MinhaFeature`
5. Abra um Pull Request

### Commits Convencionais
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes
- `chore:` tarefas de build/config

## 📚 Documentação Adicional

Explore a documentação detalhada do projeto:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura, padrões de design e boas práticas
- **[DECISIONS.md](DECISIONS.md)** - Decisões técnicas e trade-offs
- **[TESTING.md](TESTING.md)** - Guia completo de testes
- **[env.example](env.example)** - Template de variáveis de ambiente

## 📝 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para detalhes.


