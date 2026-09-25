import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import String, Numeric, Integer, DateTime, func

# 1. Base ORM
class Base(DeclarativeBase):
    pass

# 2. Modelo ORM da Tabela do Pix
class PixEstatistica(Base):
    __tablename__ = "pix_estatisticas"

    id: Mapped[int] = mapped_column(Integer, primary_primary_key=True, autoincrement=True)
    ano_mes: Mapped[str] = mapped_column(String(6), nullable=False, index=True)
    natureza: Mapped[str] = mapped_column(String(100), nullable=True)
    pagador: Mapped[str] = mapped_column(String(100), nullable=True)
    recebedor: Mapped[str] = mapped_column(String(100), nullable=True)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    valor: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False, default=0.00)
    data_carga: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

# 3. Gerenciador de Conexão
class DatabaseManager:
    def __init__(self, db_url: str = None):
        # Busca a URL do banco das variáveis de ambiente ou usa uma padrão local
        self.db_url = db_url or os.getenv(
            "DATABASE_URL", 
            "postgresql+psycopg2://postgres:postgres@localhost:5432/pix_db"
        )
        self.engine = create_engine(self.db_url, echo=False, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Cria todas as tabelas mapeadas no banco de dados, caso não existam."""
        print("🔨 Verificando e criando tabelas no PostgreSQL...")
        Base.metadata.create_all(self.engine)
        print("✅ Tabelas verificadas/criadas com sucesso!")