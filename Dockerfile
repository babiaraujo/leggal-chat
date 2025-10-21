# Multi-stage Dockerfile para Backend + Frontend no Render
FROM node:18-slim AS frontend-build

WORKDIR /frontend

# Copiar package.json e instalar dependências
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

# Copiar código do frontend
COPY frontend/ ./

# Definir variável de ambiente para o build
ENV VITE_API_URL=/
ENV NODE_ENV=production

# Fazer build do frontend
RUN npm run build

# Stage 2: Backend Python + Frontend build
FROM python:3.11-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instalar dependências do sistema (incluindo nginx para servir frontend)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    curl \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements do backend
COPY backend/requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ .

# Copiar build do frontend para o nginx
COPY --from=frontend-build /frontend/dist /usr/share/nginx/html

# Configurar nginx
RUN echo 'server { \n\
    listen 8080; \n\
    root /usr/share/nginx/html; \n\
    index index.html; \n\
    \n\
    location / { \n\
        try_files $uri $uri/ /index.html; \n\
    } \n\
    \n\
    location /api { \n\
        proxy_pass http://localhost:8000; \n\
        proxy_http_version 1.1; \n\
        proxy_set_header Upgrade $http_upgrade; \n\
        proxy_set_header Connection "upgrade"; \n\
        proxy_set_header Host $host; \n\
        proxy_set_header X-Real-IP $remote_addr; \n\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; \n\
        proxy_set_header X-Forwarded-Proto $scheme; \n\
    } \n\
    \n\
    location /auth { \n\
        proxy_pass http://localhost:8000; \n\
        proxy_http_version 1.1; \n\
        proxy_set_header Host $host; \n\
        proxy_set_header X-Real-IP $remote_addr; \n\
    } \n\
    \n\
    location /tasks { \n\
        proxy_pass http://localhost:8000; \n\
        proxy_http_version 1.1; \n\
        proxy_set_header Host $host; \n\
        proxy_set_header X-Real-IP $remote_addr; \n\
    } \n\
    \n\
    location /chat { \n\
        proxy_pass http://localhost:8000; \n\
        proxy_http_version 1.1; \n\
        proxy_set_header Host $host; \n\
        proxy_set_header X-Real-IP $remote_addr; \n\
    } \n\
    \n\
    location /health { \n\
        proxy_pass http://localhost:8000; \n\
    } \n\
}' > /etc/nginx/sites-available/default

# Script de inicialização
RUN echo '#!/bin/bash\n\
nginx &\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000' > /start.sh && \
chmod +x /start.sh

# Expor portas (Render usa PORT env var, geralmente 10000)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Comando de inicialização
CMD ["/start.sh"]

