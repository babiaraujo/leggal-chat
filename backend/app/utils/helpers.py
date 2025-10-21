"""
Funções auxiliares reutilizáveis
"""

from app.constants import (
    PRIORITY_TRANSLATION,
    STATUS_TRANSLATION,
    PRIORITY_EMOJIS,
)


def translate_priority(priority: str) -> str:
    """Traduz prioridade para português"""
    return PRIORITY_TRANSLATION.get(priority, priority)


def translate_status(status: str) -> str:
    """Traduz status para português"""
    return STATUS_TRANSLATION.get(status, status)


def get_priority_emoji(priority: str) -> str:
    """Retorna emoji da prioridade"""
    return PRIORITY_EMOJIS.get(priority, "⚪")


def format_task_summary(task) -> str:
    """Formata resumo de uma tarefa para exibição"""
    priority_emoji = get_priority_emoji(task.priority)
    priority_text = translate_priority(task.priority)
    status_text = translate_status(task.status)
    
    description = task.description or "Sem descrição"
    
    return (
        f"{priority_emoji} **{task.title}**\n"
        f"   └─ {description}\n"
        f"   ├─ Status: {status_text}\n"
        f"   └─ Prioridade: {priority_text}"
    )

