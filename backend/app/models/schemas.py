from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .models import Priority, TaskStatus


class UserBase(BaseModel):
    email: str  # Simplificado para funcionar sem email-validator
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: str  # Simplificado para funcionar sem email-validator
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    raw_message: Optional[str] = None
    priority: Optional[Priority] = Priority.MEDIUM
    status: Optional[TaskStatus] = TaskStatus.PENDING


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    id: str
    ai_title: Optional[str] = None
    ai_summary: Optional[str] = None
    ai_priority: Optional[Priority] = None
    ai_reasoning: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: str

    class Config:
        from_attributes = True


class TaskFilters(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    search: Optional[str] = None
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)


class WebhookPayload(BaseModel):
    message: str
    from_user: Optional[str] = None
    timestamp: Optional[str] = None


class AIAnalysisResult(BaseModel):
    title: str
    summary: str
    suggested_priority: Priority
    reasoning: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class SearchResult(BaseModel):
    task: TaskResponse
    similarity: float


class TaskStats(BaseModel):
    by_status: dict[str, int]
    by_priority: dict[str, int]
    total: int
