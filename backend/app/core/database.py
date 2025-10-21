from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Configuração da engine do SQLAlchemy
connect_args = {}
if "sqlite" in settings.database_url:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.environment == "development",
    connect_args=connect_args
)

# SessionLocal para operações de banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
Base = declarative_base()


def get_db():
    """
    Dependency para obter sessão do banco de dados
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Cria todas as tabelas no banco de dados
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        raise


def drop_tables():
    """
    Remove todas as tabelas do banco de dados (apenas para desenvolvimento)
    """
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ Tabelas removidas com sucesso")
    except Exception as e:
        print(f"❌ Erro ao remover tabelas: {e}")
        raise


def test_connection():
    """
    Testa conexão com o banco de dados
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Conexão com banco de dados estabelecida")
            return True
    except Exception as e:
        print(f"❌ Erro de conexão com banco: {e}")
        return False
