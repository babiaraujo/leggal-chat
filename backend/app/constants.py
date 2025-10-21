"""
Constantes globais da aplicação
"""

# Prioridades de tarefas
PRIORITY_LOW = "LOW"
PRIORITY_MEDIUM = "MEDIUM"
PRIORITY_HIGH = "HIGH"
PRIORITY_URGENT = "URGENT"

# Status de tarefas
STATUS_PENDING = "PENDING"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_COMPLETED = "COMPLETED"
STATUS_CANCELLED = "CANCELLED"

# Traduções PT-BR
PRIORITY_TRANSLATION = {
    PRIORITY_LOW: "Baixa",
    PRIORITY_MEDIUM: "Média",
    PRIORITY_HIGH: "Alta",
    PRIORITY_URGENT: "Urgente",
}

STATUS_TRANSLATION = {
    STATUS_PENDING: "Pendente",
    STATUS_IN_PROGRESS: "Em progresso",
    STATUS_COMPLETED: "Concluída",
    STATUS_CANCELLED: "Cancelada",
}

# Emojis de prioridade
PRIORITY_EMOJIS = {
    PRIORITY_LOW: "🟢",
    PRIORITY_MEDIUM: "🟡",
    PRIORITY_HIGH: "🟠",
    PRIORITY_URGENT: "🔴",
}

# Palavras-chave para classificação de mensagens
CONVERSATION_KEYWORDS = [
    'oi', 'olá', 'ola', 'hey', 'e aí', 'eai', 'tudo bem', 'tudo bom',
    'bom dia', 'boa tarde', 'boa noite', 'obrigad', 'valeu', 'vlw',
    'legal', 'show', 'massa', 'top', 'maneiro', 'dahora',
    'vsf', 'pqp', 'cacete', 'caramba', 'nossa', 'mds', 'ai ai',
    'help', 'ajuda', 'socorro', 'perdid', 'confus',
    'como funciona', 'o que você faz', 'quem é você', 'como usar'
]

QUESTION_KEYWORDS = [
    'qual', 'quais', 'como', 'quando', 'onde', 'por que', 'porque',
    'quanto', 'quantos', 'quantas', 'o que', 'há', 'existe', 'tem',
    'posso', 'pode', 'consegue', 'me mostra', 'me diz', 'me conta',
    'vê', 'veja', 'mostra', 'lista'
]

ACTION_KEYWORDS = [
    'preciso', 'devo', 'tenho que', 'precisa', 'fazer', 'criar',
    'organizar', 'preparar', 'revisar', 'enviar', 'comprar',
    'agendar', 'marcar', 'ligar', 'falar com'
]

