from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.settings import secrets
from app.database.db import init_db,engine
from app.proceder.v1.users.crud.crud import create_admin

from app.proceder.v1.users.routes import routes as user_route

from app.proceder.v1.users.models.models import ProcederUsers

# Configuração do FastAPI
app = FastAPI()

# Configuração do CORS (para o React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cria o banco de dados ao iniciar o app
@app.on_event("startup")
async def on_startup():
    await init_db()
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        username = secrets['ADMIN_USER']
        email = secrets['ADMIN_EMAIL']
        password = secrets['ADMIN_PASSWORD']
        
        await create_admin(session=session, username=username, email=email, password=password)
        
app.include_router(user_route.router, prefix="/admin")