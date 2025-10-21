from fastapi import APIRouter, Depends, HTTPException, status
from ..models.schemas import AIAnalysisResult
from ..services.ai_service import ai_service

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/analyze")
async def analyze_message(message: str) -> AIAnalysisResult:
    """
    Analisa uma mensagem usando IA e retorna título, resumo e prioridade sugerida
    """
    try:
        result = await ai_service.analyze_task(message)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na análise de IA: {str(e)}"
        )


@router.post("/search")
async def semantic_search(query: str, limit: int = 5):
    """
    Busca semântica em tarefas usando embeddings
    """
    try:
        # Esta rota seria usada para buscar tarefas similares
        # sem precisar de autenticação específica
        return {
            "query": query,
            "limit": limit,
            "message": "Busca semântica implementada no endpoint /tasks/search/similar"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na busca semântica: {str(e)}"
        )
