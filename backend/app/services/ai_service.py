import json
import re
from typing import List, Dict, Any, Optional, TYPE_CHECKING
from ..core.config import settings
from ..models.schemas import AIAnalysisResult
from ..models.models import Priority

if TYPE_CHECKING:
    from ..models.models import Task

# Tentar importar OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class AIService:
    def __init__(self):
        # Verificar se OpenAI está disponível e configurada
        self.openai_available = OPENAI_AVAILABLE and bool(settings.openai_api_key)
        if self.openai_available:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = getattr(settings, 'openai_model_name', 'gpt-4o-mini')
            print(f"✅ OpenAI configurada com modelo {self.model}")
        else:
            print("⚠️  OpenAI não disponível, usando análise simplificada")

    async def analyze_task(self, message: str) -> AIAnalysisResult:
        """
        Analisa uma mensagem e gera título, resumo e prioridade sugerida
        Usa OpenAI se disponível, caso contrário usa análise simplificada
        """
        try:
            if self.openai_available:
                return await self._analyze_with_openai(message)
            else:
                return self._analyze_simplified(message)

        except Exception as e:
            print(f"Erro na análise de IA: {e}")
            # Retornar análise padrão em caso de erro
            return AIAnalysisResult(
                title=message[:50] + "..." if len(message) > 50 else message,
                summary=message[:100] + "..." if len(message) > 100 else message,
                suggested_priority=Priority.MEDIUM,
                reasoning="Erro na análise automática",
                confidence=0.3
            )
    
    async def _analyze_with_openai(self, message: str) -> AIAnalysisResult:
        """Análise usando OpenAI GPT"""
        prompt = f"""Analise a seguinte mensagem de tarefa e forneça:
1. Um título conciso (máximo 60 caracteres)
2. Um resumo breve (máximo 150 caracteres)
3. Prioridade sugerida (LOW, MEDIUM, HIGH, ou URGENT)
4. Raciocínio para a prioridade escolhida

Mensagem: {message}

Responda APENAS com um JSON no formato:
{{
    "title": "título aqui",
    "summary": "resumo aqui",
    "priority": "MEDIUM",
    "reasoning": "explicação aqui"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "Você é um assistente especializado em análise e priorização de tarefas. Responda sempre em português do Brasil."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        content = response.choices[0].message.content.strip()
        
        # Extrair JSON da resposta
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            priority_str = result.get('priority', 'MEDIUM').upper()
            priority = Priority[priority_str] if priority_str in Priority.__members__ else Priority.MEDIUM
            
            return AIAnalysisResult(
                title=result.get('title', message[:60]),
                summary=result.get('summary', message[:150]),
                suggested_priority=priority,
                reasoning=result.get('reasoning', 'Análise automática por IA'),
                confidence=0.9
            )
        else:
            # Se não conseguir parsear, usar análise simplificada
            return self._analyze_simplified(message)
    
    def _analyze_simplified(self, message: str) -> AIAnalysisResult:
        """Análise simplificada baseada em palavras-chave"""
        title = self._generate_title(message)
        summary = self._generate_summary(message)
        suggested_priority = self._determine_priority(message)
        reasoning = self._generate_reasoning(message, suggested_priority)

        return AIAnalysisResult(
            title=title,
            summary=summary,
            suggested_priority=suggested_priority,
            reasoning=reasoning,
            confidence=0.7
        )

    def _generate_title(self, message: str) -> str:
        """Gera um título simples baseado na mensagem"""
        # Remove pontuação e limita o tamanho
        clean_message = re.sub(r'[^\w\s]', '', message).strip()
        words = clean_message.split()[:8]  # Máximo 8 palavras
        return ' '.join(words) if words else "Nova tarefa"

    def _generate_summary(self, message: str) -> str:
        """Gera um resumo simples"""
        if len(message) > 100:
            return message[:97] + "..."
        return message

    def _determine_priority(self, message: str) -> Priority:
        """Determina prioridade baseada em palavras-chave"""
        message_lower = message.lower()

        urgent_keywords = ['urgente', 'asap', 'hoje', 'agora', 'imediato', 'crítico']
        high_keywords = ['importante', 'reunião', 'prazo', 'deadline', 'cliente']
        low_keywords = ['talvez', 'quando possível', 'baixa prioridade']

        if any(keyword in message_lower for keyword in urgent_keywords):
            return Priority.URGENT
        elif any(keyword in message_lower for keyword in high_keywords):
            return Priority.HIGH
        elif any(keyword in message_lower for keyword in low_keywords):
            return Priority.LOW
        else:
            return Priority.MEDIUM

    def _generate_reasoning(self, message: str, priority: Priority) -> str:
        """Gera explicação da prioridade"""
        if priority == Priority.URGENT:
            return "Palavras indicam urgência (urgente, asap, hoje, etc.)"
        elif priority == Priority.HIGH:
            return "Palavras indicam importância (reunião, prazo, cliente)"
        elif priority == Priority.LOW:
            return "Palavras indicam baixa prioridade"
        else:
            return "Prioridade padrão atribuída automaticamente"

    async def search_similar_tasks(self, query: str, tasks: List[Any], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Busca tarefas similares usando busca textual simples
        Versão simplificada que funciona sem embeddings
        """
        try:
            if not tasks:
                return []

            query_lower = query.lower()
            results = []

            for task in tasks:
                # Combinar vários campos para busca mais rica
                text_parts = []
                if task.title:
                    text_parts.append(task.title)
                if task.description:
                    text_parts.append(task.description)
                if task.ai_title:
                    text_parts.append(task.ai_title)
                if task.ai_summary:
                    text_parts.append(task.ai_summary)
                if task.raw_message:
                    text_parts.append(task.raw_message)

                task_text = " ".join(text_parts).lower()

                # Calcular similaridade simples baseada em palavras comuns
                query_words = set(query_lower.split())
                task_words = set(task_text.split())

                # Jaccard similarity (interseção sobre união)
                if query_words or task_words:
                    intersection = len(query_words.intersection(task_words))
                    union = len(query_words.union(task_words))
                    similarity = intersection / union if union > 0 else 0.0
                else:
                    similarity = 0.0

                if similarity > 0.1:  # Threshold mínimo de similaridade
                    results.append({
                        "task": task,
                        "similarity": similarity
                    })

            # Ordenar por similaridade
            results.sort(key=lambda x: x["similarity"], reverse=True)

            return results[:top_k]

        except Exception as e:
            print(f"Erro na busca semântica: {e}")
            return []

# Instância global do serviço de IA
ai_service = AIService()
