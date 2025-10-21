/**
 * Constantes de prioridades de tarefas
 */

export const PRIORITY_CONFIG = {
  LOW: {
    emoji: '🟢',
    text: 'Baixa',
    color: 'green',
  },
  MEDIUM: {
    emoji: '🟡',
    text: 'Média',
    color: 'yellow',
  },
  HIGH: {
    emoji: '🟠',
    text: 'Alta',
    color: 'orange',
  },
  URGENT: {
    emoji: '🔴',
    text: 'Urgente',
    color: 'red',
  },
} as const

export const STATUS_CONFIG = {
  PENDING: {
    text: 'Pendente',
    color: 'gray',
  },
  IN_PROGRESS: {
    text: 'Em Progresso',
    color: 'blue',
  },
  COMPLETED: {
    text: 'Concluída',
    color: 'green',
  },
  CANCELLED: {
    text: 'Cancelada',
    color: 'red',
  },
} as const

export type Priority = keyof typeof PRIORITY_CONFIG
export type TaskStatus = keyof typeof STATUS_CONFIG

