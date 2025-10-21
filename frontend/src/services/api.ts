import axios from 'axios'
import {
  User,
  Task,
  TaskCreate,
  TaskUpdate,
  TaskFilters,
  AIAnalysisResult,
  SearchResult,
  AuthResponse,
  TaskStats
} from '../types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para adicionar token JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Serviço de autenticação
export const authService = {
  async register(email: string, password: string, name?: string): Promise<User> {
    const response = await api.post<User>('/auth/register', {
      email,
      password,
      name,
    })
    return response.data
  },

  async login(email: string, password: string): Promise<AuthResponse> {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const response = await api.post<AuthResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return response.data
  },

  async getProfile(): Promise<User> {
    const response = await api.get<User>('/auth/me')
    return response.data
  },
}

// Serviço de tarefas
export const taskService = {
  async getTasks(filters?: TaskFilters): Promise<Task[]> {
    const params = new URLSearchParams()

    if (filters?.status) params.append('status', filters.status)
    if (filters?.priority) params.append('priority', filters.priority)
    if (filters?.search) params.append('search', filters.search)
    if (filters?.limit) params.append('limit', filters.limit.toString())
    if (filters?.offset) params.append('offset', filters.offset.toString())

    const response = await api.get<Task[]>(`/tasks?${params}`)
    return response.data
  },

  async getTask(id: string): Promise<Task> {
    const response = await api.get<Task>(`/tasks/${id}`)
    return response.data
  },

  async createTask(task: TaskCreate): Promise<Task> {
    const response = await api.post<Task>('/tasks', task)
    return response.data
  },

  async updateTask(id: string, task: TaskUpdate): Promise<Task> {
    const response = await api.put<Task>(`/tasks/${id}`, task)
    return response.data
  },

  async deleteTask(id: string): Promise<void> {
    await api.delete(`/tasks/${id}`)
  },

  async getStats(): Promise<TaskStats> {
    const response = await api.get<TaskStats>('/tasks/stats/overview')
    return response.data
  },

  async searchSimilar(query: string, limit: number = 5): Promise<SearchResult[]> {
    const response = await api.get<SearchResult[]>(`/tasks/search/similar?query=${encodeURIComponent(query)}&limit=${limit}`)
    return response.data
  },
}

// Serviço de IA
export const aiService = {
  async analyzeMessage(message: string): Promise<AIAnalysisResult> {
    const response = await api.post<AIAnalysisResult>(`/ai/analyze?message=${encodeURIComponent(message)}`)
    return response.data
  },
}

// Serviço de Chat Agêntico
export interface ChatResponse {
  type: 'answer' | 'task_created'
  content: string
  task?: Task | null
}

export interface ChatHistoryMessage {
  id: string
  message: string
  is_user: boolean
  task_id: string | null
  created_at: string
}

export const chatService = {
  async sendMessage(message: string): Promise<ChatResponse> {
    const response = await api.post<ChatResponse>('/chat/message', { message })
    return response.data
  },
  
  async getHistory(limit: number = 50): Promise<ChatHistoryMessage[]> {
    const response = await api.get<ChatHistoryMessage[]>(`/chat/history?limit=${limit}`)
    return response.data
  },
}

export default api
