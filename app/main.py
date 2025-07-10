from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config.settings import secrets
from app.database.db import get_session,init_db,engine
from app.users.crud.users import create_admin

from app.users.routes import routes as user_route

# Configuração do FastAPI
app = FastAPI()

# Configuração do CORS (para o React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
        username_enviroment = f'ADMIN_USER'
        email_enviroment = f'ADMIN_EMAIL'
        password_enviroment = f'ADMIN_PASSWORD'
        
        username = secrets[username_enviroment]
        email = secrets[email_enviroment]
        password = secrets[password_enviroment]
        
        await create_admin(session=session, username=username, email=email, password=password)
        
app.include_router(user_route.router, prefix="/admin")