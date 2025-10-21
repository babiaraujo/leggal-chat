#!/bin/bash

# Script de verificação rápida do sistema
echo "🔍 Verificando sistema Leggal..."
echo "============================================="

# Verificar Docker
echo "🐳 Verificando Docker..."
if command -v docker &> /dev/null; then
    echo "✅ Docker instalado"
    if docker info &> /dev/null; then
        echo "✅ Docker rodando"
    else
        echo "❌ Docker não está rodando"
        exit 1
    fi
else
    echo "❌ Docker não instalado"
    exit 1
fi

# Verificar Docker Compose
echo ""
echo "🐳 Verificando Docker Compose..."
if command -v docker-compose &> /dev/null; then
    echo "✅ Docker Compose instalado (standalone)"
    DOCKER_COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    echo "✅ Docker Compose instalado (plugin)"
    DOCKER_COMPOSE_CMD="docker compose"
else
    echo "❌ Docker Compose não encontrado"
    exit 1
fi

# Verificar containers
echo ""
echo "📦 Verificando containers..."
CONTAINERS=$($DOCKER_COMPOSE_CMD ps -q 2>/dev/null)
if [ -n "$CONTAINERS" ]; then
    echo "✅ Containers rodando:"
    $DOCKER_COMPOSE_CMD ps
else
    echo "⚠️  Containers não estão rodando"
    echo "💡 Execute: ./start.sh ou docker-compose up -d"
fi

# Testar serviços
echo ""
echo "🔗 Testando serviços..."

# PostgreSQL
if $DOCKER_COMPOSE_CMD exec -T postgres pg_isready -U leggal_user -d leggal_db &> /dev/null; then
    echo "✅ PostgreSQL OK"
else
    echo "❌ PostgreSQL com problemas ou não está rodando"
fi

# Redis
if $DOCKER_COMPOSE_CMD exec -T redis redis-cli ping &> /dev/null; then
    echo "✅ Redis OK"
else
    echo "❌ Redis com problemas ou não está rodando"
fi

# Backend API
if curl -f -s http://localhost:8000/health &> /dev/null; then
    echo "✅ Backend API OK"
    echo "📚 Documentação: http://localhost:8000/docs"
else
    echo "❌ Backend API com problemas ou não está rodando"
    if [ -n "$CONTAINERS" ]; then
        echo "📊 Últimos logs da API:"
        $DOCKER_COMPOSE_CMD logs --tail=10 backend
    fi
fi

# Frontend
if curl -f -s http://localhost:5173 &> /dev/null 2>&1; then
    echo "✅ Frontend OK"
else
    echo "⚠️  Frontend não está rodando (executar localmente)"
    echo "💡 cd frontend && npm install && npm run dev"
fi

# Verificar .env
echo ""
echo "📝 Verificando configuração..."
if [ -f "backend/.env" ]; then
    if grep -q "sk-your-api-key-here" backend/.env 2>/dev/null || grep -q "your-secret-key-here" backend/.env 2>/dev/null; then
        echo "⚠️  Chave OpenAI ou SECRET_KEY não configurada"
        echo "💡 Copie env.example para backend/.env e configure as variáveis"
    else
        echo "✅ Configuração OK"
    fi
else
    echo "❌ Arquivo backend/.env não encontrado"
    echo "💡 Copie: cp env.example backend/.env"
fi

echo ""
echo "============================================="
echo "🎯 Status do Sistema:"
echo ""
echo "🖥️  Backend:"
echo "   └─ API: http://localhost:8000"
echo "   └─ Docs: http://localhost:8000/docs"
echo "   └─ Health: http://localhost:8000/health"
echo ""
echo "🌐 Frontend:"
echo "   └─ App: http://localhost:5173"
echo ""
echo "💡 Comandos úteis:"
echo "   └─ Iniciar: ./start.sh"
echo "   └─ Parar: docker-compose down"
echo "   └─ Logs: docker-compose logs -f"
echo "   └─ Limpar: ./scripts/clean.sh"
echo ""
