from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
import uuid
from ..models.models import Task, User, Priority, TaskStatus
from ..models.schemas import TaskCreate, TaskUpdate, TaskFilters, TaskStats
from .ai_service import ai_service


class TaskService:
    @staticmethod
    async def create_task(db: Session, user_id: str, task_data: TaskCreate) -> Task:
        """Cria uma nova tarefa"""
        # Analisar tarefa com IA
        ai_analysis = await ai_service.analyze_task(task_data.raw_message or task_data.title)

        # Criar tarefa no banco
        db_task = Task(
            id=str(uuid.uuid4()),
            title=task_data.title,
            description=task_data.description,
            raw_message=task_data.raw_message,
            priority=task_data.priority,
            status=task_data.status,
            user_id=user_id,
            ai_title=ai_analysis.title,
            ai_summary=ai_analysis.summary,
            ai_priority=ai_analysis.suggested_priority,
            ai_reasoning=ai_analysis.reasoning
        )

        db.add(db_task)
        db.commit()
        db.refresh(db_task)

        return db_task

    @staticmethod
    def get_tasks(
        db: Session,
        user_id: str,
        filters: TaskFilters
    ) -> List[Task]:
        """Lista tarefas com filtros"""

        query = db.query(Task).filter(Task.user_id == user_id)

        # Aplicar filtros
        if filters.status:
            query = query.filter(Task.status == filters.status)

        if filters.priority:
            query = query.filter(Task.priority == filters.priority)

        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term),
                    Task.raw_message.ilike(search_term),
                    Task.ai_title.ilike(search_term),
                    Task.ai_summary.ilike(search_term)
                )
            )

        # Ordenar por data de criação (mais recentes primeiro)
        query = query.order_by(Task.created_at.desc())

        # Aplicar paginação
        query = query.offset(filters.offset).limit(filters.limit)

        return query.all()

    @staticmethod
    def get_task_by_id(db: Session, task_id: str, user_id: str) -> Optional[Task]:
        """Busca tarefa por ID"""
        return db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()

    @staticmethod
    def update_task(
        db: Session,
        task_id: str,
        user_id: str,
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """Atualiza uma tarefa"""
        db_task = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not db_task:
            return None

        # Atualizar campos
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        db.commit()
        db.refresh(db_task)

        return db_task

    @staticmethod
    def delete_task(db: Session, task_id: str, user_id: str) -> bool:
        """Deleta uma tarefa"""
        result = db.query(Task).filter(
            and_(Task.id == task_id, Task.user_id == user_id)
        ).delete()

        db.commit()
        return result > 0

    @staticmethod
    def get_task_stats(db: Session, user_id: str) -> TaskStats:
        """Obtém estatísticas das tarefas"""
        # Estatísticas por status
        status_stats = db.query(
            Task.status,
            func.count(Task.id).label('count')
        ).filter(Task.user_id == user_id).group_by(Task.status).all()

        # Estatísticas por prioridade
        priority_stats = db.query(
            Task.priority,
            func.count(Task.id).label('count')
        ).filter(Task.user_id == user_id).group_by(Task.priority).all()

        # Total de tarefas
        total = db.query(func.count(Task.id)).filter(Task.user_id == user_id).scalar()

        return TaskStats(
            by_status={status.value: count for status, count in status_stats},
            by_priority={priority.value: count for priority, count in priority_stats},
            total=total or 0
        )

    @staticmethod
    async def search_similar_tasks(
        db: Session,
        query: str,
        user_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Busca tarefas similares usando IA"""
        # Buscar tarefas do usuário
        tasks = db.query(Task).filter(Task.user_id == user_id).all()

        # Usar serviço de IA para busca semântica
        similar_tasks = await ai_service.search_similar_tasks(query, tasks, limit)

        return similar_tasks
