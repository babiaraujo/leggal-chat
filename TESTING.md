# 🧪 Guia de Testes - Leggal

> Guia completo para testar o assistente inteligente de produtividade

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Início Rápido](#início-rápido)
- [Testes do Backend](#testes-do-backend)
- [Testes do Frontend](#testes-do-frontend)
- [Testes de Integração](#testes-de-integração)
- [Testes Manuais](#testes-manuais)
- [Troubleshooting](#troubleshooting)

---

## Pré-requisitos

### Essenciais
- ✅ Docker & Docker Compose
- ✅ Chave API do OpenAI
- ✅ Git (opcional)

### Para desenvolvimento
- ✅ Python 3.11+
- ✅ Node.js 18+
- ✅ PostgreSQL 15+ (local ou Docker)

---

## Início Rápido

### 1. Clone e Configure

```bash
git clone <repository-url>
cd test-leggal

# Configurar OpenAI API key
cd backend
cp .env.example .env
# Edite .env e adicione sua chave OpenAI
```

### 2. Inicie com Docker

```bash
# Voltar para raiz
cd ..

# Iniciar todos os serviços
docker-compose up -d

# Aguardar inicialização
sleep 30

# Verificar status
docker-compose ps
```

### 3. Inicializar Banco de Dados

```bash
cd backend
PYTHONPATH=. python scripts/init.py
```

### 4. Acessar a Aplicação

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Credenciais de teste**:
- Email: `teste@leggal.com`
- Senha: `123456`

---

## Testes do Backend

### Testes Automatizados

```bash
cd backend

# Executar todos os testes
pytest

# Com cobertura
pytest --cov=app --cov-report=html

# Testes específicos
pytest tests/test_auth.py -v

# Testes com output verboso
pytest -vv
```

### Testes de API

#### 1. Health Check

```bash
curl http://localhost:8000/health
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "timestamp": 1234567890,
  "database": "connected"
}
```

#### 2. Registro de Usuário

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "novo@leggal.com",
    "password": "senha123",
    "name": "Novo Usuário"
  }'
```

#### 3. Login

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=teste@leggal.com&password=123456"
```

**Salve o token JWT retornado:**
```bash
export TOKEN="seu_token_jwt_aqui"
```

#### 4. Perfil do Usuário

```bash
curl http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

#### 5. Listar Tarefas

```bash
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer $TOKEN"
```

#### 6. Criar Tarefa

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "Revisar contrato urgente",
    "description": "Revisar contrato do cliente X",
    "priority": "URGENT"
  }'
```

#### 7. Chat com IA (Conversação)

```bash
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Olá! Quantas tarefas tenho pendentes?"
  }'
```

#### 8. Chat com IA (Criar Tarefa)

```bash
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Preciso comprar material de escritório urgente amanhã"
  }'
```

#### 9. Histórico de Chat

```bash
curl http://localhost:8000/chat/history \
  -H "Authorization: Bearer $TOKEN"
```

#### 10. Atualizar Status de Tarefa

```bash
curl -X PUT http://localhost:8000/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "status": "IN_PROGRESS"
  }'
```

### Testes de Segurança

#### Teste 1: Acesso sem autenticação (deve falhar)

```bash
curl http://localhost:8000/tasks
# Deve retornar 401 Unauthorized
```

#### Teste 2: Token inválido (deve falhar)

```bash
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer token_invalido"
# Deve retornar 401 Unauthorized
```

#### Teste 3: Validação de dados

```bash
# Email inválido (deve falhar)
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "email-invalido",
    "password": "123",
    "name": "Test"
  }'
# Deve retornar 422 Validation Error
```

---

## Testes do Frontend

### Desenvolvimento Local

```bash
cd frontend

# Instalar dependências
npm install

# Executar servidor dev
npm run dev

# Build de produção
npm run build

# Preview do build
npm run preview
```

### Testes Automatizados

```bash
cd frontend

# Executar testes
npm test

# Com cobertura
npm test -- --coverage

# Watch mode
npm test -- --watch
```

### Linting e Formatação

```bash
# Verificar erros de lint
npx eslint src/ --ext .ts,.tsx

# Fix automático
npx eslint src/ --ext .ts,.tsx --fix

# Formatar código
npx prettier --write "src/**/*.{ts,tsx,css}"

# Verificar formatação
npx prettier --check "src/**/*.{ts,tsx,css}"
```

### Testes Manuais (UI)

#### 1. Login
- Acessar http://localhost:5173/login
- Inserir credenciais de teste
- Verificar redirecionamento para chat

#### 2. Chat com IA
- Enviar mensagem: "Olá!"
- Verificar resposta da IA
- Enviar: "Preciso comprar café urgente"
- Verificar criação de tarefa

#### 3. Lista de Tarefas
- Clicar em "Tarefas" no header
- Verificar lista de tarefas
- Testar filtros (Ativas/Concluídas)
- Clicar em "Iniciar" em uma tarefa
- Clicar em "Concluir"
- Clicar em "Reabrir"

#### 4. Perfil
- Clicar em "Perfil"
- Verificar informações do usuário
- Testar logout

#### 5. Persistência de Chat
- Enviar várias mensagens
- Recarregar página
- Verificar histórico mantido

---

## Testes de Integração

### Fluxo Completo E2E

```bash
# 1. Registrar usuário
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "e2e@test.com",
    "password": "test123",
    "name": "E2E Test"
  }'

# 2. Login
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=e2e@test.com&password=test123" \
  | jq -r '.access_token')

# 3. Criar tarefa via chat
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Preciso revisar proposta comercial urgente"
  }'

# 4. Listar tarefas
curl http://localhost:8000/tasks \
  -H "Authorization: Bearer $TOKEN"

# 5. Fazer pergunta ao chat
curl -X POST http://localhost:8000/chat/message \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "message": "Quantas tarefas urgentes tenho?"
  }'
```

---

## Testes Manuais

### Cenários de Uso Real

#### Cenário 1: Novo Usuário

1. Acessar /register
2. Criar conta
3. Fazer login
4. Ver boas-vindas do chat
5. Criar primeira tarefa via chat
6. Verificar tarefa na lista

#### Cenário 2: Gerenciamento de Tarefas

1. Criar 5 tarefas diferentes
2. Marcar 2 como "Em Progresso"
3. Concluir 1 tarefa
4. Filtrar por "Ativas"
5. Filtrar por "Concluídas"
6. Reabrir tarefa concluída

#### Cenário 3: Chat Inteligente

1. Fazer pergunta: "Quais tarefas tenho hoje?"
2. Criar tarefa: "Comprar material"
3. Fazer pergunta: "Quantas urgentes?"
4. Reagir com: "Obrigado!"
5. Verificar respostas contextuais

---

## Troubleshooting

### Backend não inicia

```bash
# Verificar logs
docker-compose logs backend

# Verificar se porta está ocupada
lsof -i :8000

# Reiniciar serviço
docker-compose restart backend
```

### Banco de dados não conecta

```bash
# Verificar PostgreSQL
docker-compose logs postgres

# Testar conexão
docker-compose exec postgres psql -U leggal_user -d leggal_db -c "SELECT 1;"

# Recriar banco
docker-compose down -v
docker-compose up -d
```

### Frontend não carrega

```bash
# Verificar node_modules
cd frontend && npm install

# Limpar cache
rm -rf node_modules .vite
npm install

# Verificar porta
lsof -i :5173
```

### OpenAI não responde

```bash
# Verificar chave no .env
cat backend/.env | grep OPENAI_API_KEY

# Testar chave manualmente
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Erro 403 Forbidden

```bash
# Verificar token JWT
echo $TOKEN

# Gerar novo token
# Fazer login novamente
```

### Mensagens não aparecem no chat

```bash
# Verificar se tabela existe
docker-compose exec postgres psql -U leggal_user -d leggal_db \
  -c "\dt chat_messages"

# Recriar tabelas
cd backend && PYTHONPATH=. python scripts/init.py
```

---

## Comandos Úteis

### Docker

```bash
# Ver todos os containers
docker-compose ps

# Logs em tempo real
docker-compose logs -f

# Logs de um serviço específico
docker-compose logs -f backend

# Reiniciar tudo
docker-compose restart

# Parar tudo
docker-compose down

# Limpar volumes
docker-compose down -v
```

### Banco de Dados

```bash
# Acessar PostgreSQL
docker-compose exec postgres psql -U leggal_user -d leggal_db

# Backup
docker exec postgres pg_dump -U leggal_user leggal_db > backup.sql

# Restore
docker exec -i postgres psql -U leggal_user leggal_db < backup.sql
```

### Limpeza

```bash
# Limpar cache Python
find . -type d -name "__pycache__" -exec rm -rf {} +

# Limpar node_modules
rm -rf frontend/node_modules

# Limpar tudo
./scripts/clean.sh --deep
```

---

## Métricas de Qualidade

### Cobertura de Testes

**Target**: >70% de cobertura

```bash
cd backend
pytest --cov=app --cov-report=term-missing
```

### Performance

**Targets**:
- API latency P95: <100ms
- Frontend load time: <2s
- Chat response time: <1s

```bash
# Benchmark simples
time curl http://localhost:8000/health
```

---

## Checklist de Testes

### Pré-Deploy

- [ ] Todos os testes automatizados passando
- [ ] Cobertura de testes >70%
- [ ] Linting sem erros
- [ ] Build de produção funciona
- [ ] Docker Compose sobe sem erros
- [ ] Documentação atualizada

### Funcional

- [ ] Registro e login funcionam
- [ ] Chat responde perguntas
- [ ] Chat cria tarefas
- [ ] Tarefas podem ser gerenciadas
- [ ] Filtros funcionam
- [ ] Histórico é persistido
- [ ] Logout funciona

### Não-Funcional

- [ ] Performance adequada
- [ ] Sem memory leaks
- [ ] CORS configurado
- [ ] HTTPS ready (produção)
- [ ] Logs estruturados
- [ ] Healthchecks funcionam

---

**🎉 Com esses testes, você garante qualidade e confiabilidade total!**

**Última atualização**: Outubro 2024
