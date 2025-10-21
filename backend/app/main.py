from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import time
import logging

from .core.config import settings
from .core.database import create_tables
from .routers import auth, tasks, webhook, ai, chat


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["200/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicação Leggal Task Manager")

    if settings.environment == "development":
        logger.info("📊 Criando tabelas no banco de dados")
        create_tables()

    logger.info("Inicializando serviços de IA...")

    yield

    logger.info("Encerrando aplicação")


app = FastAPI(
    title="Leggal Task Manager API",
    description="API para gerenciamento de tarefas com integração de IA",
    version="1.0.0",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.leggal.com", "localhost"]
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"{request.method} {request.url.path}")

    try:
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        process_time = time.time() - start_time
        logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")

        return response
    
    except Exception as e:
        logger.error(f"❌ {request.method} {request.url.path} - Error: {type(e).__name__}")
        
        if settings.environment == "production":
            return Response(
                content='{"detail":"Internal server error"}',
                status_code=500,
                media_type="application/json"
            )
        raise


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "environment": settings.environment
    }


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
