export interface User {
  id: string
  email: string
  name?: string
  created_at: string
  updated_at: string
}

export interface Task {
  id: string
  title: string
  description?: string
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED'
  raw_message?: string
  ai_title?: string
  ai_summary?: string
  ai_priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  ai_reasoning?: string
  created_at: string
  updated_at: string
  user_id: string
}

export interface TaskCreate {
  title: string
  description?: string
  raw_message?: string
  priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  status?: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED'
}

export interface TaskUpdate {
  title?: string
  description?: string
  priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  status?: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED'
}

export interface TaskFilters {
  status?: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED'
  priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  search?: string
  limit?: number
  offset?: number
}

export interface AIAnalysisResult {
  title: string
  summary: string
  suggested_priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'URGENT'
  reasoning: string
  confidence: number
}

export interface SearchResult {
  task: Task
  similarity: number
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface TaskStats {
  by_status: Record<string, number>
  by_priority: Record<string, number>
  total: number
}
