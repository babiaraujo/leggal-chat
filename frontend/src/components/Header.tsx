import { Link, useLocation } from 'react-router-dom'
import { MessageSquare, CheckSquare, User, LogOut } from 'lucide-react'
import { useAuth } from '../hooks/useAuth'
import { Logo } from './Logo'

export function Header() {
  const location = useLocation()
  const { logout } = useAuth()

  const isActive = (path: string) => location.pathname === path

  return (
    <header className="bg-white shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-2 sm:px-3">
        <div className="flex items-center justify-between h-12">
          {/* Logo - Menor e mais compacto */}
          <Link to="/" className="flex items-center flex-shrink-0 mr-2">
            <Logo className="h-5 text-green-600 hover:text-green-700 transition-colors" />
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-0.5 sm:space-x-1">
            <Link
              to="/"
              className={`flex items-center space-x-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg transition-colors ${
                isActive('/')
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <MessageSquare className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="font-medium text-sm sm:text-base">Chat IA</span>
            </Link>

            <Link
              to="/tasks"
              className={`flex items-center space-x-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg transition-colors ${
                isActive('/tasks')
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <CheckSquare className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="font-medium text-sm sm:text-base">Tarefas</span>
            </Link>

            <Link
              to="/profile"
              className={`flex items-center space-x-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg transition-colors ${
                isActive('/profile')
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <User className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="font-medium text-sm sm:text-base">Perfil</span>
            </Link>

            <button
              onClick={logout}
              className="flex items-center space-x-1.5 px-2.5 sm:px-3 py-1.5 rounded-lg text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors ml-0.5 sm:ml-1"
            >
              <LogOut className="w-4 h-4 sm:w-5 sm:h-5" />
              <span className="font-medium text-sm sm:text-base">Sair</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
  )
}

