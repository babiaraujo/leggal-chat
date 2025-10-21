/**
 * Funções utilitárias para formatação
 */

/**
 * Converte markdown simples para HTML
 * Suporta: **negrito**, quebras de linha
 */
export function formatMarkdown(text: string): string {
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n/g, '<br />')
}

/**
 * Formata data para exibição
 */
export function formatTime(date: Date): string {
  return date.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

/**
 * Formata data completa
 */
export function formatDate(date: Date): string {
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

/**
 * Formata data e hora
 */
export function formatDateTime(date: Date): string {
  return `${formatDate(date)} às ${formatTime(date)}`
}

