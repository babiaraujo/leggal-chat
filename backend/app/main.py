from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

from .core.config import settings
from .core.database import create_tables
from .routers import auth, tasks, webhook, ai, chat


# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação"""
    # Startup
    logger.info("🚀 Iniciando aplicação Leggal Task Manager")

    # Criar tabelas no banco (apenas para desenvolvimento)
    if settings.environment == "development":
        logger.info("📊 Criando tabelas no banco de dados")
        create_tables()

    # Inicializar serviços de IA
    logger.info("🤖 Inicializando serviços de IA...")
    # ai_service será inicializado quando usado pela primeira vez

    yield

    # Shutdown
    logger.info("🛑 Encerrando aplicação")


# Criar aplicação FastAPI
app = FastAPI(
    title="Leggal Task Manager API",
    description="API para gerenciamento de tarefas com integração de IA",
    version="1.0.0",
    lifespan=lifespan
)


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Configurar hosts confiáveis
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.leggal.com", "localhost"]
    )


# Middleware para logging de requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    # Log da requisição
    logger.info(f"📨 {request.method} {request.url.path}")

    response = await call_next(request)

    # Tempo de processamento
    process_time = time.time() - start_time
    logger.info(f"📨 {request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")

    return response


# Health check
@app.get("/health", tags=["health"])
def health_check():
    """Verifica se a aplicação está funcionando"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.environment
    }


# Rotas da API
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(webhook.router)
app.include_router(ai.router)
app.include_router(chat.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level="info"
    )
