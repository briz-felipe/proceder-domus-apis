# db.py
import os
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Configuração do SQLite assíncrono (arquivo `database.db` na raiz do projeto)
DATABASE_URL = "sqlite+aiosqlite:///database.db"

# Cria a engine assíncrona
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Logs no terminal (útil para desenvolvimento)
    pool_recycle=1800,  # Recicla conexões após 1800 segundos (evita timeouts)
    pool_pre_ping=True,  # Testa conexões antes de usar (evita erros)
)

# Cria uma fábrica de sessões assíncronas
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Cria as tabelas no banco de dados (se não existirem)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency para injetar sessões em rotas FastAPI
async def get_session():
    async with async_session() as session:
        yield session
        
        
        