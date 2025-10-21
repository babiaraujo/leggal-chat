import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User } from '../types'
import { authService } from '../services/api'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, name?: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

export const useAuth = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        set({ isLoading: true })
        try {
          const response = await authService.login(email, password)
          
          // Armazenar token ANTES de buscar o perfil
          localStorage.setItem('token', response.access_token)
          set({ token: response.access_token })
          
          const user = await authService.getProfile()

          set({
            user,
            token: response.access_token,
            isAuthenticated: true,
            isLoading: false,
          })
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      register: async (email: string, password: string, name?: string) => {
        set({ isLoading: true })
        try {
          await authService.register(email, password, name)
          // Após registro, fazer login automaticamente
          await get().login(email, password)
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },

      logout: () => {
        localStorage.removeItem('token')
        set({
          user: null,
          token: null,
          isAuthenticated: false,
        })
      },

      checkAuth: async () => {
        const token = localStorage.getItem('token')
        if (!token) {
          set({ isAuthenticated: false, user: null, token: null })
          return
        }

        try {
          const user = await authService.getProfile()
          set({
            user,
            token,
            isAuthenticated: true,
          })
        } catch (error) {
          // Token inválido, limpar estado
          localStorage.removeItem('token')
          set({ isAuthenticated: false, user: null, token: null })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({ user: state.user, token: state.token }),
    }
  )
)
