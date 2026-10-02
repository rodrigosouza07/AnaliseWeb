import os

from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    create_engine,
    String,
    Numeric,
    Integer,
    DateTime,
    func,
    text
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker
)


# ============================================================
# 1. BASE ORM
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# 2. MODELO ORM - ESTATÍSTICAS DO PIX
# ============================================================

class PixEstatistica(Base):

    __tablename__ = "pix_estatisticas"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    ano_mes: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
        index=True
    )

    natureza: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    pagador: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    recebedor: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    quantidade: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    valor: Mapped[Decimal] = mapped_column(
        Numeric(18, 2),
        nullable=False,
        default=Decimal("0.00")
    )

    data_carga: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )


# ============================================================
# 3. GERENCIADOR DO BANCO
# ============================================================

class DatabaseManager:

    def __init__(self, db_url: str | None = None):

        self.db_url = db_url or os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:1712@localhost:5432/pix_db"
        )

        print("🔧 Configurando conexão PostgreSQL...")

        self.engine = create_engine(
            self.db_url,
            echo=False,
            pool_pre_ping=True
        )

        self.SessionLocal = sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False
        )

        print("✅ Engine SQLAlchemy criado!")

    # ========================================================
    # TESTAR CONEXÃO
    # ========================================================

    def test_connection(self):

        print("🔌 Testando conexão com PostgreSQL...")

        try:

            with self.engine.connect() as connection:

                result = connection.execute(
                    text("SELECT 1")
                )

                print(
                    f"🔎 PostgreSQL respondeu: {result.scalar()}"
                )

            print("✅ Conexão com PostgreSQL funcionando!")

            return True

        except Exception as e:

            print(
                f"❌ Erro na conexão com PostgreSQL:\n{e}"
            )

            return False

    # ========================================================
    # CRIAR TABELAS
    # ========================================================

    def create_tables(self):

        print("🔨 Verificando e criando tabelas...")

        try:

            Base.metadata.create_all(
                self.engine
            )

            print(
                "✅ Tabelas verificadas/criadas com sucesso!"
            )

            return True

        except Exception as e:

            print(
                f"❌ Erro ao criar tabelas:\n{e}"
            )

            return False

    # ========================================================
    # CRIAR SESSÃO
    # ========================================================

    def get_session(self):

        return self.SessionLocal()


# ============================================================
# 4. TESTE DO BANCO
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🚀 TESTE DO BANCO DE DADOS")
    print("=" * 60)

    db = DatabaseManager()

    print()

    # Testa PostgreSQL
    conectado = db.test_connection()

    print()

    if conectado:

        # Cria tabela
        db.create_tables()

    else:

        print(
            "⚠️ Tabelas não serão criadas "
            "porque o banco não está acessível."
        )

    print()
    print("=" * 60)
    print("🏁 TESTE FINALIZADO")
    print("=" * 60)