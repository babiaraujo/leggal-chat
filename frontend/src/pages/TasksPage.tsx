import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { CheckCircle2, Clock, Circle, Play, Check, RotateCcw } from 'lucide-react'

import { taskService } from '../services/api'
import { Header } from '../components/Header'
import { PRIORITY_CONFIG } from '../constants/priorities'
import type { Task } from '../types'

type FilterStatus = 'ACTIVE' | 'COMPLETED'
type TaskStatusUpdate = 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED'

export default function TasksPage() {
  const queryClient = useQueryClient()
  const [filterStatus, setFilterStatus] = useState<FilterStatus>('ACTIVE')

  // Query para buscar tarefas
  const { data: allTasks, isLoading } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => taskService.getTasks(),
  })

  // Mutation para atualizar status
  const updateStatusMutation = useMutation({
    mutationFn: ({ taskId, status }: { taskId: string; status: TaskStatusUpdate }) =>
      taskService.updateTask(taskId, { status }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  // Filtrar tarefas por status
  const filteredTasks = allTasks?.filter((task: Task) => {
    if (filterStatus === 'ACTIVE') {
      return task.status === 'PENDING' || task.status === 'IN_PROGRESS'
    }
    return task.status === 'COMPLETED'
  })

  // Contar tarefas por categoria
  const activeCount = allTasks?.filter(
    (t) => t.status === 'PENDING' || t.status === 'IN_PROGRESS'
  ).length || 0
  const completedCount = allTasks?.filter((t) => t.status === 'COMPLETED').length || 0

  // Handlers
  const handleStatusUpdate = (taskId: string, status: TaskStatusUpdate) => {
    updateStatusMutation.mutate({ taskId, status })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
      <Header />

      <div className="max-w-5xl mx-auto px-4 py-8">
        {/* Cabeçalho */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Minhas Tarefas</h1>
          <p className="text-gray-600">Organize e gerencie suas atividades</p>
        </header>

        {/* Filtros de Status */}
        {allTasks && allTasks.length > 0 && (
          <div className="flex gap-2 mb-6">
            <FilterButton
              active={filterStatus === 'ACTIVE'}
              onClick={() => setFilterStatus('ACTIVE')}
              icon="🔥"
              label="Ativas"
              count={activeCount}
              variant="blue"
            />
            <FilterButton
              active={filterStatus === 'COMPLETED'}
              onClick={() => setFilterStatus('COMPLETED')}
              icon="✅"
              label="Concluídas"
              count={completedCount}
              variant="green"
            />
          </div>
        )}

        {/* Lista de Tarefas */}
        {isLoading ? (
          <LoadingSpinner />
        ) : filteredTasks && filteredTasks.length > 0 ? (
          <div className="space-y-3">
            {filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onStatusUpdate={handleStatusUpdate}
                isUpdating={updateStatusMutation.isPending}
              />
            ))}
          </div>
        ) : (
          <EmptyState status={filterStatus} />
        )}
      </div>
    </div>
  )
}

// ============================================================================
// Componentes auxiliares
// ============================================================================

interface FilterButtonProps {
  active: boolean
  onClick: () => void
  icon: string
  label: string
  count: number
  variant: 'blue' | 'green'
}

function FilterButton({ active, onClick, icon, label, count, variant }: FilterButtonProps) {
  const variantClasses = {
    blue: active ? 'bg-blue-600 text-white shadow-md' : 'bg-white text-gray-700 hover:bg-gray-50',
    green: active ? 'bg-green-600 text-white shadow-md' : 'bg-white text-gray-700 hover:bg-gray-50',
  }

  return (
    <button
      onClick={onClick}
      className={`flex-1 py-3 px-4 rounded-lg font-medium transition-all ${variantClasses[variant]}`}
    >
      <div className="flex items-center justify-center gap-2">
        <span>
          {icon} {label}
        </span>
        <span className="text-sm">({count})</span>
      </div>
    </button>
  )
}

interface TaskCardProps {
  task: Task
  onStatusUpdate: (taskId: string, status: TaskStatusUpdate) => void
  isUpdating: boolean
}

function TaskCard({ task, onStatusUpdate, isUpdating }: TaskCardProps) {
  const priorityInfo = PRIORITY_CONFIG[task.priority as keyof typeof PRIORITY_CONFIG]

  return (
    <div className="bg-white rounded-lg shadow-sm p-5 hover:shadow-md transition-all border border-gray-100">
      <div className="flex items-start gap-4">
        {/* Ícone de Status */}
        <div className="flex-shrink-0 mt-1">
          <TaskStatusIcon status={task.status} />
        </div>

        {/* Conteúdo */}
        <div className="flex-1 min-w-0">
          {/* Título e Prioridade */}
          <div className="flex items-start justify-between gap-4 mb-2">
            <h3
              className={`text-lg font-semibold ${
                task.status === 'COMPLETED' ? 'text-gray-500 line-through' : 'text-gray-900'
              }`}
            >
              {task.title}
            </h3>
            {priorityInfo && (
              <span className="flex-shrink-0 flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold bg-gray-50">
                <span className="text-base">{priorityInfo.emoji}</span>
                <span className="text-gray-700">{priorityInfo.text}</span>
              </span>
            )}
          </div>

          {/* Descrição */}
          {task.description && (
            <p className="text-sm text-gray-600 mb-3">{task.description}</p>
          )}

          {/* Ações */}
          <TaskActions
            taskId={task.id}
            status={task.status}
            onStatusUpdate={onStatusUpdate}
            isUpdating={isUpdating}
          />
        </div>
      </div>
    </div>
  )
}

interface TaskActionsProps {
  taskId: string
  status: string
  onStatusUpdate: (taskId: string, status: TaskStatusUpdate) => void
  isUpdating: boolean
}

function TaskActions({ taskId, status, onStatusUpdate, isUpdating }: TaskActionsProps) {
  const buttonClass = "flex items-center gap-2 px-3 py-1.5 rounded-lg transition-colors text-sm font-medium disabled:opacity-50"

  if (status === 'PENDING') {
    return (
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => onStatusUpdate(taskId, 'IN_PROGRESS')}
          disabled={isUpdating}
          className={`${buttonClass} bg-blue-50 text-blue-700 hover:bg-blue-100`}
        >
          <Play className="w-4 h-4" />
          Iniciar
        </button>
        <button
          onClick={() => onStatusUpdate(taskId, 'COMPLETED')}
          disabled={isUpdating}
          className={`${buttonClass} bg-green-50 text-green-700 hover:bg-green-100`}
        >
          <Check className="w-4 h-4" />
          Concluir
        </button>
      </div>
    )
  }

  if (status === 'IN_PROGRESS') {
    return (
      <button
        onClick={() => onStatusUpdate(taskId, 'COMPLETED')}
        disabled={isUpdating}
        className={`${buttonClass} bg-green-50 text-green-700 hover:bg-green-100`}
      >
        <Check className="w-4 h-4" />
        Concluir
      </button>
    )
  }

  if (status === 'COMPLETED') {
    return (
      <button
        onClick={() => onStatusUpdate(taskId, 'PENDING')}
        disabled={isUpdating}
        className={`${buttonClass} bg-gray-50 text-gray-700 hover:bg-gray-100`}
      >
        <RotateCcw className="w-4 h-4" />
        Reabrir
      </button>
    )
  }

  return null
}

function TaskStatusIcon({ status }: { status: string }) {
  if (status === 'COMPLETED') {
    return <CheckCircle2 className="w-6 h-6 text-green-500" />
  }
  if (status === 'IN_PROGRESS') {
    return <Clock className="w-6 h-6 text-blue-500" />
  }
  return <Circle className="w-6 h-6 text-gray-400" />
}

function LoadingSpinner() {
  return (
    <div className="flex justify-center py-12">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600" />
    </div>
  )
}

function EmptyState({ status }: { status: FilterStatus }) {
  const messages = {
    ACTIVE: {
      emoji: '🎉',
      title: 'Nenhuma tarefa ativa no momento!',
      subtitle: 'Envie uma mensagem no chat para criar sua primeira tarefa!',
    },
    COMPLETED: {
      emoji: '✨',
      title: 'Nenhuma tarefa concluída ainda.',
      subtitle: 'Conclua algumas tarefas para vê-las aqui!',
    },
  }

  const message = messages[status]

  return (
    <div className="text-center py-12 bg-white rounded-xl border border-gray-100">
      <p className="text-gray-600 text-lg mb-2">
        {message.emoji} {message.title}
      </p>
      <p className="text-gray-400 text-sm">{message.subtitle}</p>
    </div>
  )
}
