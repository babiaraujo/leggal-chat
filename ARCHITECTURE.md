# 🏗️ Arquitetura e Boas Práticas

## Visão Geral da Arquitetura

### Backend (FastAPI)

```
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Auth    │  │  Tasks   │  │   Chat   │   Routers  │
│  │  Router  │  │  Router  │  │  Router  │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼──────────────┼──────────────────┘
        │             │              │
┌───────▼─────────────▼──────────────▼──────────────────┐
│                 Service Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   Auth   │  │   Task   │  │    AI    │  Services  │
│  │  Service │  │  Service │  │  Service │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼──────────────┼──────────────────┘
        │             │              │
┌───────▼─────────────▼──────────────▼──────────────────┐
│               Repository Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   User   │  │   Task   │  │   Chat   │   Models   │
│  │  Model   │  │  Model   │  │  Model   │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼──────────────┼──────────────────┘
        │             │              │
        └─────────────▼──────────────┘
                      │
              ┌───────▼────────┐
              │   PostgreSQL   │
              └────────────────┘
```

### Frontend (React)

```
┌─────────────────────────────────────────────────────────┐
│                   Presentation Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Login   │  │  Tasks   │  │   Chat   │   Pages    │
│  │  Page    │  │  Page    │  │  Page    │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼──────────────┼──────────────────┘
        │             │              │
┌───────▼─────────────▼──────────────▼──────────────────┐
│                 Component Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  Header  │  │ TaskCard │  │  Message │ Components │
│  │   Logo   │  │  Button  │  │  Bubble  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
└────────────────────────────────────────────────────────┘
        │             │              │
┌───────▼─────────────▼──────────────▼──────────────────┐
│                  Service Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │   API    │  │   Auth   │  │   Query  │  Services  │
│  │ Service  │  │   Hook   │  │  Client  │            │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘            │
└───────┼─────────────┼──────────────┼──────────────────┘
        │             │              │
        └─────────────▼──────────────┘
                      │
              ┌───────▼────────┐
              │  Backend API   │
              └────────────────┘
```

## Princípios de Design

### 1. Separation of Concerns (SoC)

**Backend:**
- **Routers**: Apenas definição de endpoints e validação de entrada
- **Services**: Lógica de negócios e orquestração
- **Models**: Representação de dados e queries ao banco
- **Schemas**: Validação e serialização de dados

**Frontend:**
- **Pages**: Composição de componentes e gerenciamento de estado de página
- **Components**: Componentes reutilizáveis e isolados
- **Hooks**: Lógica de estado e efeitos colaterais
- **Services**: Comunicação com API

### 2. Single Responsibility Principle (SRP)

Cada módulo/função tem uma única responsabilidade:

```python
# ❌ Ruim: Faz demais
def handle_user_login(email, password):
    # Valida
    # Autentica
    # Atualiza cache
    # Envia email
    # Registra log
    pass

# ✅ Bom: Responsabilidades separadas
def validate_credentials(email, password):
    pass

def authenticate_user(email, password):
    pass

def send_welcome_email(user):
    pass
```

### 3. Dependency Injection

**Backend (FastAPI):**
```python
# Dependencies para injeção
async def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    # Lógica de autenticação
    return user

# Uso nos endpoints
@router.get("/tasks")
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return TaskService.get_tasks(db, current_user.id)
```

### 4. Repository Pattern

Isolar acesso a dados:

```python
# ❌ Ruim: Query direto no service
class TaskService:
    @staticmethod
    def get_tasks(db: Session, user_id: str):
        return db.query(Task).filter(Task.user_id == user_id).all()

# ✅ Bom: Repository pattern
class TaskRepository:
    @staticmethod
    def find_by_user(db: Session, user_id: str):
        return db.query(Task).filter(Task.user_id == user_id).all()

class TaskService:
    @staticmethod
    def get_tasks(db: Session, user_id: str):
        return TaskRepository.find_by_user(db, user_id)
```

### 5. DTO Pattern

Validação com Pydantic:

```python
# Schema de entrada
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    priority: Priority = Priority.MEDIUM

# Schema de saída
class TaskResponse(BaseModel):
    id: str
    title: str
    priority: Priority
    created_at: datetime

    class Config:
        from_attributes = True
```

## Boas Práticas

### Backend

#### 1. Type Hints Sempre
```python
# ✅ Bom
def calculate_priority(urgency: int, impact: int) -> str:
    return "HIGH" if urgency > 7 else "MEDIUM"

# ❌ Ruim
def calculate_priority(urgency, impact):
    return "HIGH" if urgency > 7 else "MEDIUM"
```

#### 2. Constantes Centralizadas
```python
# constants.py
PRIORITY_URGENT = "URGENT"
PRIORITY_HIGH = "HIGH"
PRIORITY_MEDIUM = "MEDIUM"
PRIORITY_LOW = "LOW"
```

#### 3. Error Handling Consistente
```python
from fastapi import HTTPException, status

# ✅ Bom
def get_task(db: Session, task_id: str, user_id: str) -> Task:
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return task
```

#### 4. Logging Estruturado
```python
import logging

logger = logging.getLogger(__name__)

def process_message(message: str):
    logger.info(f"Processing message", extra={
        "message_length": len(message),
        "timestamp": datetime.now().isoformat()
    })
```

#### 5. Async Quando Possível
```python
# ✅ Bom para I/O
async def call_openai_api(prompt: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(...)
        return response.json()

# ✅ Bom para CPU-bound
def calculate_embeddings(text: str) -> list:
    # Operação síncrona intensiva
    return model.encode(text)
```

### Frontend

#### 1. Component Organization
```typescript
// ✅ Bom: Props tipadas, funções auxiliares separadas
interface TaskCardProps {
  task: Task
  onUpdate: (id: string, status: TaskStatus) => void
}

function TaskCard({ task, onUpdate }: TaskCardProps) {
  // Lógica do componente
}

// Componentes auxiliares no mesmo arquivo (se pequenos)
function TaskActions({ taskId, status }: TaskActionsProps) {
  // Sub-componente
}
```

#### 2. Custom Hooks
```typescript
// ✅ Bom: Lógica reutilizável
function useTaskFilter(tasks: Task[], filter: FilterStatus) {
  return useMemo(() => {
    return tasks.filter(task => {
      if (filter === 'ACTIVE') {
        return task.status === 'PENDING' || task.status === 'IN_PROGRESS'
      }
      return task.status === 'COMPLETED'
    })
  }, [tasks, filter])
}
```

#### 3. Constants e Utils
```typescript
// constants/priorities.ts
export const PRIORITY_CONFIG = {
  LOW: { emoji: '🟢', text: 'Baixa' },
  MEDIUM: { emoji: '🟡', text: 'Média' },
  HIGH: { emoji: '🟠', text: 'Alta' },
  URGENT: { emoji: '🔴', text: 'Urgente' },
} as const

// utils/formatters.ts
export function formatMarkdown(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br />')
}
```

#### 4. React Query Patterns
```typescript
// ✅ Bom: Queries e mutations organizadas
function useTasks() {
  const queryClient = useQueryClient()

  const { data: tasks, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: taskService.getTasks,
  })

  const updateMutation = useMutation({
    mutationFn: taskService.updateTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  return { tasks, isLoading, updateTask: updateMutation.mutate }
}
```

#### 5. Error Boundaries
```typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true }
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught:', error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback />
    }
    return this.props.children
  }
}
```

## Performance

### Backend
- **Database Indexes**: Campos de busca frequente
- **Query Optimization**: Evitar N+1 queries
- **Caching**: Redis para dados frequentes
- **Async I/O**: Operações de rede assíncronas
- **Connection Pooling**: Pool de conexões ao banco

### Frontend
- **Code Splitting**: Lazy loading de rotas
- **Memoization**: useMemo e useCallback
- **Virtualization**: Para listas grandes
- **Image Optimization**: Lazy loading de imagens
- **Bundle Size**: Tree shaking e minificação

## Segurança

### Backend
- **Input Validation**: Pydantic schemas
- **SQL Injection**: Sempre usar ORM
- **Authentication**: JWT com refresh tokens
- **Rate Limiting**: Limitar requests por IP
- **CORS**: Configurar origens permitidas
- **Secrets**: Nunca commitar .env

### Frontend
- **XSS Prevention**: Sanitizar HTML
- **CSRF Protection**: Tokens CSRF
- **Secure Storage**: HttpOnly cookies
- **Input Validation**: Validar no frontend também
- **HTTPS**: Sempre em produção

## Testes

### Backend
```python
# test_task_service.py
def test_create_task_success(db_session):
    # Arrange
    user = create_test_user(db_session)
    task_data = TaskCreate(
        title="Test Task",
        priority="HIGH"
    )
    
    # Act
    task = TaskService.create_task(db_session, user.id, task_data)
    
    # Assert
    assert task.title == "Test Task"
    assert task.priority == "HIGH"
    assert task.user_id == user.id
```

### Frontend
```typescript
// TaskCard.test.tsx
describe('TaskCard', () => {
  it('should render task details', () => {
    const task = createMockTask()
    render(<TaskCard task={task} onUpdate={jest.fn()} />)
    
    expect(screen.getByText(task.title)).toBeInTheDocument()
    expect(screen.getByText(/Iniciar/i)).toBeInTheDocument()
  })
})
```

## Conclusão

Esta arquitetura prioriza:
- ✅ **Manutenibilidade**: Código fácil de entender e modificar
- ✅ **Escalabilidade**: Preparado para crescer
- ✅ **Testabilidade**: Fácil de testar
- ✅ **Segurança**: Proteções em todas as camadas
- ✅ **Performance**: Otimizado por design

