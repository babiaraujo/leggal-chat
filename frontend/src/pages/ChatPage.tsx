import { useState, useEffect, useRef } from 'react'
import { Send, Loader2, Bot, User } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'

import { useAuth } from '../hooks/useAuth'
import { chatService } from '../services/api'
import { Header } from '../components/Header'
import { formatMarkdown, formatTime } from '../utils/formatters'

interface Message {
  id: string
  text: string
  isUser: boolean
  timestamp: Date
}

export function ChatPage() {
  const { user } = useAuth()
  const [messages, setMessages] = useState<Message[]>([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  // Buscar histórico de mensagens
  const { data: history } = useQuery({
    queryKey: ['chatHistory'],
    queryFn: () => chatService.getHistory(),
  })

  // Carregar histórico quando disponível
  useEffect(() => {
    if (history && history.length > 0) {
      const loadedMessages: Message[] = history.map((msg) => ({
        id: msg.id,
        text: msg.message,
        isUser: msg.is_user,
        timestamp: new Date(msg.created_at),
      }))
      setMessages(loadedMessages)
    } else if (messages.length === 0) {
      // Mensagem de boas-vindas apenas se não houver histórico
      setMessages([getWelcomeMessage(user?.name)])
    }
  }, [history, user?.name])

  // Auto-scroll para última mensagem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Auto-resize textarea
  useEffect(() => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto'
      inputRef.current.style.height = `${Math.min(inputRef.current.scrollHeight, 120)}px`
    }
  }, [inputText])

  // Handlers
  const handleSendMessage = async () => {
    if (!inputText.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      isUser: true,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputText('')
    setIsLoading(true)

    try {
      const response = await chatService.sendMessage(inputText)

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: response.content,
        isUser: false,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, botMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: '❌ Ops! Houve um erro ao processar sua mensagem. Tente novamente.',
        isUser: false,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <Header />

      {/* Área de Mensagens */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        <div className="max-w-6xl mx-auto px-2 sm:px-3 py-3 space-y-2.5">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {isLoading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input de Mensagem */}
      <div className="bg-white border-t border-gray-200 shadow-lg">
        <div className="max-w-6xl mx-auto p-2 sm:p-3">
          <div className="flex items-end gap-2 sm:gap-3">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                rows={1}
                className="w-full px-3 sm:px-4 py-2.5 sm:py-3 bg-gray-50 border border-gray-300 rounded-2xl focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent resize-none transition-all text-sm sm:text-base"
                placeholder="Digite sua mensagem..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={handleKeyPress}
                disabled={isLoading}
                style={{ maxHeight: '120px' }}
              />
            </div>
            <button
              onClick={handleSendMessage}
              className="flex-shrink-0 w-11 h-11 sm:w-12 sm:h-12 bg-green-600 text-white rounded-full hover:bg-green-700 active:scale-95 transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100 flex items-center justify-center shadow-lg"
              disabled={isLoading || !inputText.trim()}
              aria-label="Enviar mensagem"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// Componentes auxiliares
// ============================================================================

interface MessageBubbleProps {
  message: Message
}

function MessageBubble({ message }: MessageBubbleProps) {
  return (
    <div
      className={`flex gap-2 ${message.isUser ? 'justify-end' : 'justify-start'} animate-fade-in`}
    >
      {/* Avatar do bot (apenas para mensagens do bot) */}
      {!message.isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center shadow-md">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}

      <div
        className={`group relative max-w-[75%] sm:max-w-[70%] md:max-w-[60%] rounded-2xl px-4 py-3 shadow-md transition-all hover:shadow-lg ${
          message.isUser
            ? 'bg-green-600 text-white rounded-tr-sm'
            : 'bg-white text-gray-800 rounded-tl-sm'
        }`}
      >
        {/* Conteúdo da mensagem */}
        <div
          className={`prose prose-sm max-w-none ${
            message.isUser ? 'prose-invert' : ''
          }`}
          dangerouslySetInnerHTML={{
            __html: formatMarkdown(message.text),
          }}
        />

        {/* Timestamp */}
        <div
          className={`flex items-center gap-1 mt-2 text-xs ${
            message.isUser ? 'text-green-100' : 'text-gray-500'
          }`}
        >
          <span>{formatTime(message.timestamp)}</span>
          {message.isUser && (
            <svg
              className="w-4 h-4"
              viewBox="0 0 16 16"
              fill="currentColor"
            >
              <path d="M13.854 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L6.5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z" />
            </svg>
          )}
        </div>
      </div>

      {/* Avatar do usuário (apenas para mensagens do usuário) */}
      {message.isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-blue-400 to-blue-600 rounded-full flex items-center justify-center shadow-md">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  )
}

function TypingIndicator() {
  return (
    <div className="flex gap-2 justify-start animate-fade-in">
      <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-br from-green-400 to-green-600 rounded-full flex items-center justify-center shadow-md">
        <Bot className="w-5 h-5 text-white" />
      </div>
      <div className="max-w-[75%] sm:max-w-[70%] md:max-w-[60%] rounded-2xl rounded-tl-sm px-4 py-3 shadow-md bg-white">
        <div className="flex items-center gap-1">
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
        </div>
      </div>
    </div>
  )
}

// ============================================================================
// Helpers
// ============================================================================

function getWelcomeMessage(userName?: string): Message {
  return {
    id: '1',
    text: `Olá, ${userName || 'usuário'}! 👋

**Estou aqui para otimizar seu tempo!** ⏰

Como assistente inteligente, vou te ajudar a:
✅ Organizar suas tarefas automaticamente
🤖 Priorizar o que é mais importante
📋 Responder perguntas sobre sua agenda
🎯 Aumentar sua produtividade

**Exemplos do que você pode me pedir:**
• "Quais tarefas estão pendentes?"
• "Preciso revisar contrato urgente do cliente X"
• "Quantas tarefas tenho hoje?"

Como posso te ajudar agora? 😊`,
    isUser: false,
    timestamp: new Date(),
  }
}
