from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.dependencies import get_db, get_current_user
from ..models.models import User, Task, ChatMessage as ChatMessageModel
from ..services.ai_service import ai_service
from ..services.task_service import TaskService
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    type: str  # "answer" ou "task_created"
    content: str
    task: dict | None = None


class ChatHistoryResponse(BaseModel):
    id: str
    message: str
    is_user: bool
    task_id: str | None
    created_at: datetime


@router.get("/history", response_model=list[ChatHistoryResponse])
async def get_chat_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retorna histórico de mensagens do usuário"""
    messages = db.query(ChatMessageModel).filter(
        ChatMessageModel.user_id == current_user.id
    ).order_by(ChatMessageModel.created_at.desc()).limit(limit).all()
    
    return [
        ChatHistoryResponse(
            id=msg.id,
            message=msg.message,
            is_user=msg.is_user,
            task_id=msg.task_id,
            created_at=msg.created_at
        )
        for msg in reversed(messages)  # Inverte para ordem cronológica
    ]


@router.post("/message", response_model=ChatResponse)
async def send_message(
    data: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Processa mensagem do chat de forma agêntica:
    - Se for pergunta: responde diretamente
    - Se for solicitação: cria tarefa
    """
    message = data.message.strip()
    
    # Salvar mensagem do usuário
    user_message = ChatMessageModel(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        message=message,
        is_user=True
    )
    db.add(user_message)
    db.commit()
    
    # Usar IA para classificar e processar
    result = await process_chat_message(message, current_user, db)
    
    # Salvar resposta da IA
    ai_message = ChatMessageModel(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        message=result.content,
        is_user=False,
        task_id=result.task.get('id') if result.task else None
    )
    db.add(ai_message)
    db.commit()
    
    return result


async def process_chat_message(message: str, user: User, db: Session) -> ChatResponse:
    """Processa mensagem com comportamento agêntico"""
    
    # Classificar tipo de mensagem
    is_question = await classify_message_type(message)
    
    if is_question:
        # Responder pergunta diretamente
        answer = await answer_question(message, user, db)
        return ChatResponse(
            type="answer",
            content=answer,
            task=None
        )
    else:
        # Criar tarefa
        from ..models.schemas import TaskCreate
        
        # Analisar com IA
        analysis = await ai_service.analyze_task(message)
        
        # Criar tarefa
        task_data = TaskCreate(
            title=analysis.title,
            description=analysis.summary,
            priority=analysis.suggested_priority,
            status="PENDING",
            raw_message=message
        )
        
        task = await TaskService.create_task(db, user.id, task_data)
        
        # Emoji e tradução da prioridade
        priority_map = {
            "LOW": {"emoji": "🟢", "text": "Baixa"},
            "MEDIUM": {"emoji": "🟡", "text": "Média"},
            "HIGH": {"emoji": "🟠", "text": "Alta"},
            "URGENT": {"emoji": "🔴", "text": "Urgente"}
        }
        
        priority_info = priority_map.get(analysis.suggested_priority, {"emoji": "⚪", "text": "Média"})
        
        response_text = f"""✅ **Tarefa criada com sucesso!**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 **Título:**
{analysis.title}

📝 **Descrição:**
{analysis.summary}

⚡ **Prioridade:** {priority_info['emoji']} **{priority_info['text']}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **Por que essa prioridade?**
{analysis.reasoning}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 **Próximos passos:**
• Foque nas tarefas urgentes (🔴) primeiro
• Organize seu tempo com base nas prioridades
• Use este assistente sempre que precisar!

Estou aqui para otimizar seu tempo! 💪"""
        
        return ChatResponse(
            type="task_created",
            content=response_text,
            task={
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status
            }
        )


async def classify_message_type(message: str) -> bool:
    """Classifica se mensagem é pergunta/conversa ou ação de criar tarefa. Retorna True se for pergunta/conversa."""
    
    message_lower = message.lower().strip()
    
    # Expressões de conversa/cumprimento/reação (NÃO criar tarefa)
    conversation_patterns = [
        'oi', 'olá', 'ola', 'hey', 'e aí', 'eai', 'tudo bem', 'tudo bom',
        'bom dia', 'boa tarde', 'boa noite', 'obrigad', 'valeu', 'vlw',
        'legal', 'show', 'massa', 'top', 'maneiro', 'dahora',
        'vsf', 'pqp', 'cacete', 'caramba', 'nossa', 'mds', 'ai ai',
        'help', 'ajuda', 'socorro', 'perdid', 'confus',
        'como funciona', 'o que você faz', 'quem é você', 'como usar'
    ]
    
    # Verifica se é expressão de conversa
    for pattern in conversation_patterns:
        if pattern in message_lower:
            return True
    
    # Palavras-chave de perguntas
    question_words = ['qual', 'quais', 'como', 'quando', 'onde', 'por que', 'porque', 
                      'quanto', 'quantos', 'quantas', 'o que', 'há', 'existe', 'tem',
                      'posso', 'pode', 'consegue', 'me mostra', 'me diz', 'me conta',
                      'vê', 'veja', 'mostra', 'lista']
    
    # Verifica se começa com palavra de pergunta ou tem ponto de interrogação
    if '?' in message:
        return True
    
    for word in question_words:
        if message_lower.startswith(word) or f' {word} ' in message_lower:
            return True
    
    # Mensagens muito curtas (< 15 caracteres) geralmente são conversas
    if len(message_lower) < 15 and not any(word in message_lower for word in ['preciso', 'fazer', 'criar', 'comprar', 'enviar', 'revisar']):
        return True
    
    # Palavras-chave explícitas de AÇÃO (criar tarefa)
    action_words = ['preciso', 'devo', 'tenho que', 'precisa', 'fazer', 'criar', 
                    'organizar', 'preparar', 'revisar', 'enviar', 'comprar', 
                    'agendar', 'marcar', 'ligar', 'falar com']
    
    for word in action_words:
        if word in message_lower:
            return False  # É uma ação, não é conversa
    
    # Por padrão, se não identificou como ação explícita, trata como conversa
    return True


async def answer_question(message: str, user: User, db: Session) -> str:
    """Responde perguntas do usuário usando LLM com contexto das tarefas"""
    from ..models.schemas import TaskFilters
    from ..core.config import settings
    
    # Buscar todas as tarefas do usuário para dar contexto à IA
    all_tasks = TaskService.get_tasks(
        db,
        user.id,
        TaskFilters(limit=100, offset=0)
    )
    
    # Mapa de tradução de prioridades
    priority_translation = {
        "LOW": "Baixa",
        "MEDIUM": "Média",
        "HIGH": "Alta",
        "URGENT": "Urgente"
    }
    
    status_translation = {
        "PENDING": "Pendente",
        "IN_PROGRESS": "Em progresso",
        "COMPLETED": "Concluída"
    }
    
    # Preparar contexto das tarefas
    tasks_context = []
    for task in all_tasks:
        priority_emoji = {
            "LOW": "🟢",
            "MEDIUM": "🟡", 
            "HIGH": "🟠",
            "URGENT": "🔴"
        }.get(task.priority, "⚪")
        
        priority_pt = priority_translation.get(task.priority, task.priority)
        status_pt = status_translation.get(task.status, task.status)
        
        tasks_context.append(f"{priority_emoji} {task.title} - {task.description or 'Sem descrição'} (Status: {status_pt}, Prioridade: {priority_pt})")
    
    tasks_summary = "\n".join(tasks_context) if tasks_context else "Nenhuma tarefa cadastrada."
    
    # Estatísticas
    stats = {
        "total": len(all_tasks),
        "pending": len([t for t in all_tasks if t.status == "PENDING"]),
        "in_progress": len([t for t in all_tasks if t.status == "IN_PROGRESS"]),
        "completed": len([t for t in all_tasks if t.status == "COMPLETED"]),
        "urgent": len([t for t in all_tasks if t.priority == "URGENT"]),
    }
    
    # Usar OpenAI para gerar resposta humana e contextual
    if settings.openai_api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
            
            system_prompt = f"""Você é um assistente inteligente de produtividade chamado Leggal.

SUA MISSÃO: Otimizar o tempo do usuário ajudando-o a gerenciar tarefas de forma eficiente.

PERSONALIDADE:
- Seja educado, prestativo e empático
- Fale de forma natural, como um humano real
- Sempre reforce que sua missão é OTIMIZAR O TEMPO da pessoa
- Dê dicas práticas de produtividade
- Parabenize conquistas e incentive ações
- Se o usuário estiver frustrado, mostre empatia e ofereça ajuda concreta
- Seja leve e bem-humorado quando apropriado
- NUNCA crie tarefas em conversas casuais

CONTEXTO DO USUÁRIO:
Nome: {user.name}
Total de tarefas: {stats['total']}
Pendentes: {stats['pending']}
Em progresso: {stats['in_progress']}
Concluídas: {stats['completed']}
Urgentes: {stats['urgent']}

TAREFAS DO USUÁRIO:
{tasks_summary}

COMO REAGIR A DIFERENTES SITUAÇÕES:
- Cumprimentos (oi, olá): Cumprimente de volta, mostre status das tarefas, ofereça ajuda
- Frustração (vsf, pqp, etc): Mostre empatia, pergunte o que aconteceu, ofereça ajuda
- Perguntas sobre tarefas: Responda com base no contexto real
- Pedido de ajuda: Ofereça sugestões práticas de organização
- Agradecimentos: Seja cordial e pergunte se precisa de mais algo

REGRAS:
- Responda SEMPRE em português do Brasil
- Use emojis para deixar a conversa mais amigável
- Seja CONCISO mas COMPLETO
- Ao listar tarefas, use **negrito** em títulos
- Sempre use prioridades em PORTUGUÊS: Baixa, Média, Alta, Urgente
- Sempre use status em PORTUGUÊS: Pendente, Em progresso, Concluída
- Sempre reforce sua missão de otimizar tempo
- Dê sugestões práticas e acionáveis
- Adapte o tom à situação (formal, casual, empático)
- Use separadores (━━━) para organizar informações quando necessário"""

            response = client.chat.completions.create(
                model=settings.openai_model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.8,
                max_tokens=800
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Erro ao usar OpenAI: {e}")
            # Fallback para resposta simples
            pass
    
    # Fallback se OpenAI não estiver disponível
    return f"""Olá! 👋 Sou seu assistente de produtividade.

📊 Status atual:
- {stats['total']} tarefas no total
- {stats['pending']} pendentes
- {stats['urgent']} urgentes

Minha missão é **otimizar seu tempo**! Como posso ajudar? 😊"""

