#!/usr/bin/env python3
"""
Script simples para testar funcionalidades básicas da API
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check OK")
            return True
        else:
            print(f"❌ Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False


def test_register():
    """Testa registro de usuário"""
    print("🔍 Testando registro de usuário...")
    try:
        data = {
            "email": "teste@leggal.com",
            "password": "123456",
            "name": "Usuário de Teste"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Registro OK: {result['email']}")
            return result
        else:
            print(f"❌ Registro falhou: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro no registro: {e}")
        return None


def test_login():
    """Testa login"""
    print("🔍 Testando login...")
    try:
        data = {
            "username": "teste@leggal.com",
            "password": "123456"
        }
        response = requests.post(f"{BASE_URL}/auth/login", data=data)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login OK: Token recebido")
            return result["access_token"]
        else:
            print(f"❌ Login falhou: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return None


def test_ai_analysis():
    """Testa análise de IA"""
    print("🔍 Testando análise de IA...")
    try:
        data = {
            "message": "Preciso revisar o contrato que recebemos hoje para desenvolvimento do sistema. É urgente!"
        }
        response = requests.post(f"{BASE_URL}/ai/analyze", json=data)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Análise de IA OK: {result['title']}")
            print(f"   Prioridade sugerida: {result['suggested_priority']}")
            return True
        else:
            print(f"❌ Análise de IA falhou: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro na análise de IA: {e}")
        return False


def test_create_task(token):
    """Testa criação de tarefa"""
    print("🔍 Testando criação de tarefa...")
    try:
        data = {
            "title": "Teste de tarefa",
            "description": "Tarefa criada via script de teste",
            "raw_message": "Criar uma tarefa de teste para validar o sistema",
            "priority": "MEDIUM"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/tasks", json=data, headers=headers)

        if response.status_code == 201:
            result = response.json()
            print(f"✅ Tarefa criada: {result['task']['title']}")
            return result["task"]["id"]
        else:
            print(f"❌ Criação de tarefa falhou: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erro na criação de tarefa: {e}")
        return None


def test_webhook():
    """Testa webhook"""
    print("🔍 Testando webhook...")
    try:
        data = {
            "message": "Nova tarefa via WhatsApp: reunião amanhã às 14h",
            "from": "whatsapp",
            "timestamp": "2024-01-01T10:00:00Z"
        }
        headers = {"x-user-id": "user_001"}  # ID do usuário de teste
        response = requests.post(f"{BASE_URL}/webhook/message", json=data, headers=headers)

        if response.status_code == 200:
            result = response.json()
            print(f"✅ Webhook OK: {result['message']}")
            return True
        else:
            print(f"❌ Webhook falhou: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro no webhook: {e}")
        return False


def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes da API Leggal Task Manager")
    print("=" * 50)

    # Teste 1: Health check
    if not test_health():
        print("❌ Sistema não está respondendo. Abortando testes.")
        sys.exit(1)

    # Teste 2: Análise de IA (não precisa autenticação)
    if not test_ai_analysis():
        print("⚠️  Análise de IA falhou, mas continuando testes...")

    # Teste 3: Registro e login
    user = test_register()
    if not user:
        print("❌ Não foi possível registrar usuário. Abortando testes.")
        sys.exit(1)

    token = test_login()
    if not token:
        print("❌ Não foi possível fazer login. Abortando testes.")
        sys.exit(1)

    # Teste 4: Criar tarefa
    task_id = test_create_task(token)
    if not task_id:
        print("⚠️  Não foi possível criar tarefa, mas continuando...")

    # Teste 5: Webhook
    if not test_webhook():
        print("⚠️  Webhook falhou, mas continuando...")

    print("=" * 50)
    print("🎉 Testes concluídos!")
    print("📚 Documentação da API: http://localhost:8000/docs")
    print("🔗 Interface (quando disponível): http://localhost:5173")


if __name__ == "__main__":
    main()
