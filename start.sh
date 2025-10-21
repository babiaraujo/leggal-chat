#!/bin/bash

# Script de inicialização completa do Leggal
echo "🚀 Iniciando Leggal..."
echo ""

# Verificar se Docker está instalado e rodando
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não está instalado. Instale o Docker primeiro."
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

if ! docker info &> /dev/null; then
    echo "❌ Docker não está rodando. Inicie o Docker Desktop primeiro."
    exit 1
fi

# Verificar se docker-compose está disponível
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose não está instalado."
    exit 1
fi

echo "✅ Docker verificado"

# Navegar para o diretório do projeto
cd "$(dirname "$0")"

# Verificar se .env existe no backend
if [ ! -f "backend/.env" ]; then
    echo ""
    echo "📝 Arquivo backend/.env não encontrado"
    if [ -f "env.example" ]; then
        echo "📋 Copiando env.example para backend/.env..."
        cp env.example backend/.env
        echo "⚠️  IMPORTANTE: Edite backend/.env e configure:"
        echo "   - OPENAI_API_KEY (obrigatório para IA)"
        echo "   - SECRET_KEY (gere uma chave segura)"
        echo ""
        read -p "Pressione ENTER para continuar depois de configurar o .env..."
    else
        echo "❌ env.example não encontrado. Crie backend/.env manualmente."
        exit 1
    fi
fi

echo ""
echo "🏗️  Construindo e iniciando serviços Docker..."
$DOCKER_COMPOSE_CMD up -d --build

# Aguardar serviços iniciarem
echo ""
echo "⏳ Aguardando serviços iniciarem (30s)..."
sleep 30

# Verificar se serviços estão saudáveis
echo ""
echo "🔍 Verificando saúde dos serviços..."
echo ""

# Testar PostgreSQL
if $DOCKER_COMPOSE_CMD exec -T postgres pg_isready -U leggal_user -d leggal_db &> /dev/null; then
    echo "✅ PostgreSQL OK"
else
    echo "❌ PostgreSQL com problemas"
    echo "📊 Verificando logs:"
    $DOCKER_COMPOSE_CMD logs --tail=20 postgres
    exit 1
fi

# Testar Redis
if $DOCKER_COMPOSE_CMD exec -T redis redis-cli ping &> /dev/null; then
    echo "✅ Redis OK"
else
    echo "❌ Redis com problemas"
    $DOCKER_COMPOSE_CMD logs --tail=20 redis
fi

# Testar Backend API
echo "⏳ Aguardando API inicializar..."
for i in {1..10}; do
    if curl -f -s http://localhost:8000/health &> /dev/null; then
        echo "✅ Backend API OK"
        break
    fi
    if [ $i -eq 10 ]; then
        echo "❌ Backend API não respondeu"
        echo "📊 Verificando logs da API:"
        $DOCKER_COMPOSE_CMD logs --tail=30 backend
        exit 1
    fi
    sleep 3
done

# Inicializar banco de dados
echo ""
echo "🗄️  Inicializando banco de dados..."
if $DOCKER_COMPOSE_CMD exec -T backend sh -c "cd /app && PYTHONPATH=/app python scripts/init.py" 2>/dev/null; then
    echo "✅ Banco de dados inicializado"
else
    echo "⚠️  Erro ao inicializar banco (pode já estar inicializado)"
fi

# Verificar se frontend precisa ser iniciado
echo ""
echo "🌐 Frontend..."
if [ -d "frontend/node_modules" ]; then
    echo "✅ Dependências do frontend instaladas"
else
    echo "⚠️  Dependências do frontend não instaladas"
    echo "💡 Execute: cd frontend && npm install && npm run dev"
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       🎉 Leggal iniciado com sucesso! 🎉                 ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""
echo "🖥️  BACKEND:"
echo "   └─ API: http://localhost:8000"
echo "   └─ Documentação: http://localhost:8000/docs"
echo "   └─ Health Check: http://localhost:8000/health"
echo ""
echo "🌐 FRONTEND:"
echo "   └─ App: http://localhost:5173"
echo "   └─ Para iniciar: cd frontend && npm run dev"
echo ""
echo "👤 CREDENCIAIS DE TESTE:"
echo "   └─ Email: teste@leggal.com"
echo "   └─ Senha: 123456"
echo ""
echo "🔧 COMANDOS ÚTEIS:"
echo "   └─ Parar: docker-compose down"
echo "   └─ Logs: docker-compose logs -f"
echo "   └─ Verificar: ./check-system.sh"
echo "   └─ Limpar: ./scripts/clean.sh"
echo ""
echo "📚 DOCUMENTAÇÃO:"
echo "   └─ README.md - Guia principal"
echo "   └─ TESTING.md - Como testar"
echo "   └─ ARCHITECTURE.md - Arquitetura"
echo ""
echo "💡 LEMBRE-SE:"
echo "   └─ Configure OPENAI_API_KEY no backend/.env"
echo "   └─ Inicie o frontend: cd frontend && npm run dev"
echo ""
