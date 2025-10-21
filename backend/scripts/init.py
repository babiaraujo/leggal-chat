#!/usr/bin/env python3
"""
Script de inicialização para desenvolvimento e testes
"""
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.core.database import create_tables, test_connection, drop_tables
from app.utils.seed import create_initial_data
# Importar modelos para que sejam registrados no Base.metadata
from app.models import models  # noqa: F401


def init_database():
    """Inicializa o banco de dados"""
    print("🚀 Inicializando banco de dados...")

    # Testar conexão
    if not test_connection():
        print("❌ Não foi possível conectar ao banco de dados")
        print("Verifique se o PostgreSQL está rodando e as configurações estão corretas")
        return False

    try:
        # Remover tabelas existentes (apenas desenvolvimento)
        print("🗑️  Removendo tabelas existentes...")
        drop_tables()

        # Criar tabelas
        print("📊 Criando tabelas...")
        create_tables()

        # Popular com dados iniciais
        print("🌱 Populando dados iniciais...")
        create_initial_data()

        print("✅ Inicialização concluída com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro durante inicialização: {e}")
        return False


def reset_database():
    """Reseta o banco de dados"""
    print("🔄 Resetando banco de dados...")

    if not test_connection():
        print("❌ Não foi possível conectar ao banco de dados")
        return False

    try:
        drop_tables()
        create_tables()
        create_initial_data()
        print("✅ Reset concluído com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro durante reset: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Inicialização do banco de dados")
    parser.add_argument("--reset", action="store_true", help="Reset completo do banco")

    args = parser.parse_args()

    if args.reset:
        reset_database()
    else:
        init_database()
