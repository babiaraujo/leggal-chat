from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..core.dependencies import get_db, get_current_user
from ..models.models import User
from ..models.schemas import (
    TaskCreate, TaskUpdate, TaskResponse, TaskFilters, TaskStats, SearchResult
)
from ..services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cria uma nova tarefa"""
    try:
        task = await TaskService.create_task(db, current_user.id, task_data)
        return TaskResponse.model_validate(task)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    status: str = Query(None, description="Filtrar por status"),
    priority: str = Query(None, description="Filtrar por prioridade"),
    search: str = Query(None, description="Termo de busca"),
    limit: int = Query(50, ge=1, le=100, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Lista tarefas com filtros opcionais"""
    filters = TaskFilters(
        status=status,
        priority=priority,
        search=search,
        limit=limit,
        offset=offset
    )

    tasks = TaskService.get_tasks(db, current_user.id, filters)
    return [TaskResponse.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Busca tarefa por ID"""
    task = TaskService.get_task_by_id(db, task_id, current_user.id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return TaskResponse.model_validate(task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Atualiza uma tarefa"""
    task = TaskService.update_task(db, task_id, current_user.id, task_data)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return TaskResponse.model_validate(task)


@router.delete("/{task_id}")
def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deleta uma tarefa"""
    deleted = TaskService.delete_task(db, task_id, current_user.id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )

    return {"message": "Tarefa deletada com sucesso"}


@router.get("/stats/overview", response_model=TaskStats)
def get_task_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtém estatísticas das tarefas do usuário"""
    return TaskService.get_task_stats(db, current_user.id)


@router.get("/search/similar", response_model=List[SearchResult])
async def search_similar_tasks(
    query: str = Query(..., description="Termo de busca semântica"),
    limit: int = Query(5, ge=1, le=20, description="Número máximo de resultados"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Busca tarefas similares usando IA"""
    similar_tasks = await TaskService.search_similar_tasks(
        db, query, current_user.id, limit
    )

    return [
        SearchResult(
            task=TaskResponse.model_validate(result["task"]),
            similarity=result["similarity"]
        )
        for result in similar_tasks
    ]
