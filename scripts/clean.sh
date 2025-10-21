#!/bin/bash

# Script de limpeza do projeto
echo "🧹 Limpando projeto Leggal..."
echo "==============================="

# Python cache
echo "🐍 Removendo cache Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete
echo "✅ Cache Python removido"

# Node modules (se necessário recriar)
if [ "$1" == "--deep" ]; then
    echo "📦 Removendo node_modules..."
    rm -rf frontend/node_modules
    echo "✅ node_modules removido"
fi

# Build artifacts
echo "🏗️  Removendo build artifacts..."
rm -rf frontend/dist
rm -rf frontend/build
rm -rf backend/dist
rm -rf backend/build
echo "✅ Build artifacts removidos"

# Logs
echo "📝 Removendo logs..."
find . -type f -name "*.log" -delete
echo "✅ Logs removidos"

echo ""
echo "✨ Limpeza concluída!"
echo ""
echo "💡 Para reinstalar dependências:"
echo "   Frontend: cd frontend && npm install"
echo "   Backend: cd backend && pip install -r requirements.txt"

