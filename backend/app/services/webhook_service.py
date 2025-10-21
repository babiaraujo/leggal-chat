from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models.schemas import WebhookPayload, TaskCreate, Priority, TaskStatus
from .task_service import TaskService


class WebhookService:
    @staticmethod
    async def process_webhook_message(db: Session, payload: WebhookPayload, user_id: str) -> Dict[str, Any]:
        """
        Processa mensagem recebida via webhook e cria tarefa automaticamente
        """
        try:
            # Criar dados da tarefa a partir da mensagem
            task_data = TaskCreate(
                title=payload.message[:100] + "..." if len(payload.message) > 100 else payload.message,
                description=payload.message,
                raw_message=payload.message,
                priority=Priority.MEDIUM,  # Prioridade padrão, pode ser ajustada pela IA
                status=TaskStatus.PENDING
            )

            # Criar tarefa
            task = await TaskService.create_task(db, user_id, task_data)

            return {
                "success": True,
                "message": "Tarefa criada com sucesso",
                "task_id": task.id,
                "title": task.title,
                "ai_priority": task.ai_priority.value if task.ai_priority else None,
                "ai_reasoning": task.ai_reasoning
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Erro ao processar mensagem: {str(e)}"
            }

    @staticmethod
    def validate_webhook_payload(payload: Dict[str, Any]) -> WebhookPayload:
        """
        Valida payload do webhook
        """
        # Implementar validação básica
        if not payload.get("message"):
            raise ValueError("Mensagem é obrigatória")

        return WebhookPayload(
            message=payload["message"],
            from_user=payload.get("from"),
            timestamp=payload.get("timestamp")
        )
