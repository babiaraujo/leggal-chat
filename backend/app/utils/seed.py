"""
Script para popular banco de dados com dados iniciais
"""
import asyncio
from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.models import User, Task, Priority, TaskStatus
from ..core.security import get_password_hash


def create_initial_data():
    """Cria dados iniciais para desenvolvimento"""
    db = SessionLocal()

    try:
        # Verificar se já existem dados
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("✅ Dados iniciais já existem")
            return

        # Criar usuário de teste
        hashed_password = get_password_hash("123456")
        test_user = User(
            id="user_001",
            email="teste@leggal.com",
            password=hashed_password,
            name="Usuário de Teste"
        )
        db.add(test_user)
        db.commit()

        print("✅ Usuário de teste criado: teste@leggal.com / 123456")

        # Criar tarefas de exemplo
        sample_tasks = [
            {
                "id": "task_001",
                "title": "Revisar contrato de desenvolvimento",
                "description": "Analisar contrato para desenvolvimento do sistema de gestão",
                "raw_message": "Preciso revisar o contrato que recebemos hoje para desenvolvimento do sistema de gestão. É urgente!",
                "priority": Priority.HIGH,
                "status": TaskStatus.PENDING,
                "ai_title": "Revisão de contrato de desenvolvimento",
                "ai_summary": "Revisar contrato recebido hoje para sistema de gestão",
                "ai_priority": Priority.HIGH,
                "ai_reasoning": "Palavras como 'urgente' e 'contrato' indicam alta prioridade"
            },
            {
                "id": "task_002",
                "title": "Preparar apresentação para reunião",
                "description": "Criar slides para apresentação da próxima reunião de equipe",
                "raw_message": "Preparar apresentação para reunião de amanhã",
                "priority": Priority.MEDIUM,
                "status": TaskStatus.IN_PROGRESS,
                "ai_title": "Preparação de apresentação",
                "ai_summary": "Criar slides para reunião de equipe amanhã",
                "ai_priority": Priority.MEDIUM,
                "ai_reasoning": "Reunião marcada para amanhã, prioridade média"
            },
            {
                "id": "task_003",
                "title": "Comprar café para escritório",
                "description": "Repor estoque de café e materiais básicos",
                "raw_message": "Estamos sem café no escritório, comprar hoje",
                "priority": Priority.LOW,
                "status": TaskStatus.PENDING,
                "ai_title": "Reposição de suprimentos",
                "ai_summary": "Comprar café e materiais básicos para escritório",
                "ai_priority": Priority.LOW,
                "ai_reasoning": "Tarefa de manutenção básica, baixa prioridade"
            }
        ]

        for task_data in sample_tasks:
            task = Task(
                user_id=test_user.id,
                **task_data
            )
            db.add(task)

        db.commit()
        print(f"✅ {len(sample_tasks)} tarefas de exemplo criadas")

    except Exception as e:
        print(f"❌ Erro ao criar dados iniciais: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_data()
