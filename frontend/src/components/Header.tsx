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
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <Logo className="h-8 text-green-600 hover:text-green-700 transition-colors" />
          </Link>

          {/* Navigation */}
          <nav className="flex items-center space-x-1">
            <Link
              to="/"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                isActive('/')
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <MessageSquare className="w-5 h-5" />
              <span className="font-medium">Chat IA</span>
            </Link>

            <Link
              to="/tasks"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                isActive('/tasks')
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <CheckSquare className="w-5 h-5" />
              <span className="font-medium">Tarefas</span>
            </Link>

            <Link
              to="/profile"
              className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors ${
                isActive('/profile')
                  ? 'bg-green-100 text-green-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <User className="w-5 h-5" />
              <span className="font-medium">Perfil</span>
            </Link>

            <button
              onClick={logout}
              className="flex items-center space-x-2 px-4 py-2 rounded-lg text-gray-600 hover:bg-red-50 hover:text-red-600 transition-colors ml-2"
            >
              <LogOut className="w-5 h-5" />
              <span className="font-medium">Sair</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
  )
}

