export function formatMarkdown(text: string): string {
  const div = document.createElement('div')
  div.textContent = text
  let escaped = div.innerHTML
  
  escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
  escaped = escaped.replace(/\n/g, '<br />')
  
  return escaped
}

export function formatTime(date: Date): string {
  return date.toLocaleTimeString('pt-BR', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function formatDate(date: Date): string {
  return date.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

export function formatDateTime(date: Date): string {
  return `${formatDate(date)} às ${formatTime(date)}`
}

