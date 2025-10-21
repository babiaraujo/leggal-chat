from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..core.dependencies import get_db, get_current_user_optional
from ..models.models import User
from ..models.schemas import WebhookPayload
from ..services.webhook_service import WebhookService

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post("/message")
async def receive_webhook_message(
    payload: WebhookPayload,
    x_user_id: str = Header(..., description="ID do usuário que receberá a tarefa"),
    db: Session = Depends(get_db)
):
    """
    Recebe mensagem via webhook e cria tarefa automaticamente

    Esta rota simula o recebimento de mensagens do WhatsApp
    """
    try:
        # Validar payload
        webhook_payload = WebhookService.validate_webhook_payload(payload.model_dump())

        # Processar mensagem e criar tarefa
        result = await WebhookService.process_webhook_message(
            db, webhook_payload, x_user_id
        )

        if result["success"]:
            return {
                "message": result["message"],
                "task": {
                    "id": result["task_id"],
                    "title": result["title"],
                    "ai_priority": result["ai_priority"],
                    "ai_reasoning": result["ai_reasoning"]
                }
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["error"]
            )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno: {str(e)}"
        )


@router.get("/test")
async def test_webhook():
    """
    Endpoint de teste para verificar se o webhook está funcionando
    """
    return {
        "status": "OK",
        "message": "Webhook está funcionando",
        "timestamp": "2024-01-01T00:00:00Z"
    }
