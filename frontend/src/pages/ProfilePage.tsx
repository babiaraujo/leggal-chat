import { User as UserIcon, Mail, Calendar, CheckCircle } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { Header } from '../components/Header'
import { useQuery } from '@tanstack/react-query'
import { taskService } from '../services/api'

export function ProfilePage() {
  const { user } = useAuth()

  // Buscar tarefas para estatísticas
  const { data: tasks } = useQuery({
    queryKey: ['tasks'],
    queryFn: () => taskService.getTasks(),
  })

  const totalTasks = tasks?.length || 0
  const completedTasks = tasks?.filter((t) => t.status === 'COMPLETED').length || 0
  const pendingTasks = tasks?.filter((t) => t.status === 'PENDING').length || 0
  const inProgressTasks = tasks?.filter((t) => t.status === 'IN_PROGRESS').length || 0

  return (
    <div className="min-h-screen bg-gray-100">
      <Header />

      <div className="max-w-3xl mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          {/* Header do Perfil */}
          <div className="bg-gradient-to-r from-green-600 to-green-700 px-8 py-12 text-center">
            <div className="inline-flex items-center justify-center w-24 h-24 bg-white rounded-full mb-4 shadow-lg">
              <UserIcon className="w-12 h-12 text-green-600" />
            </div>
            <h1 className="text-3xl font-bold text-white mb-2">{user?.name || 'Usuário'}</h1>
            <p className="text-green-100">{user?.email}</p>
          </div>

          {/* Informações do Perfil */}
          <div className="px-8 py-6 space-y-6">
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Informações da Conta</h2>
              <div className="space-y-4">
                <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                  <div className="flex-shrink-0 w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                    <UserIcon className="w-5 h-5 text-green-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Nome</p>
                    <p className="font-medium text-gray-900">{user?.name || '-'}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                  <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                    <Mail className="w-5 h-5 text-blue-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Email</p>
                    <p className="font-medium text-gray-900">{user?.email || '-'}</p>
                  </div>
                </div>

                <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-lg">
                  <div className="flex-shrink-0 w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                    <Calendar className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Membro desde</p>
                    <p className="font-medium text-gray-900">
                      {user?.created_at
                        ? new Date(user.created_at).toLocaleDateString('pt-BR', {
                            day: '2-digit',
                            month: 'long',
                            year: 'numeric',
                          })
                        : '-'}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            {/* Estatísticas */}
            <div>
              <h2 className="text-lg font-semibold text-gray-900 mb-4">Suas Estatísticas</h2>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-1">{totalTasks}</div>
                  <p className="text-sm text-gray-700">Total</p>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold text-green-600 mb-1">{completedTasks}</div>
                  <p className="text-sm text-gray-700">Concluídas</p>
                </div>

                <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold text-yellow-600 mb-1">{inProgressTasks}</div>
                  <p className="text-sm text-gray-700">Em Progresso</p>
                </div>

                <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-4 text-center">
                  <div className="text-3xl font-bold text-gray-600 mb-1">{pendingTasks}</div>
                  <p className="text-sm text-gray-700">Pendentes</p>
                </div>
              </div>
            </div>

            {/* Taxa de Conclusão */}
            {totalTasks > 0 && (
              <div>
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Progresso</h2>
                <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="w-5 h-5 text-green-600" />
                      <span className="font-semibold text-gray-900">Taxa de Conclusão</span>
                    </div>
                    <span className="text-2xl font-bold text-green-600">
                      {Math.round((completedTasks / totalTasks) * 100)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                    <div
                      className="bg-gradient-to-r from-green-500 to-green-600 h-full rounded-full transition-all duration-500"
                      style={{ width: `${(completedTasks / totalTasks) * 100}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-gray-600 mt-3 text-center">
                    Você completou {completedTasks} de {totalTasks} tarefas! 🎉
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
