from sqlalchemy.ext.asyncio import AsyncSession
from app.proceder.v1.users.models.models import ProcederUsers as User
from sqlalchemy.future import select
from fastapi import HTTPException, status
from passlib.hash import bcrypt
from app.proceder.v1.users.exceptions.exceptions import ProcederException, ProcederCodeException
from app.logger import logger


async def user_exists(username:str,email:str,session:AsyncSession) -> None:
    try:
        query = select(User).where((User.username == username) | (User.email == email))
        result = await session.execute(query)
        return result.scalars().first()
    except Exception as e:
        logger.error(f"v1/users/crud/crud.py:user_exists -  Error checking if user exists: {e}")
        raise ProcederException(
            procederException=ProcederCodeException.server_error
        ) from e


async def get_user_by_id(user_id:str,session:AsyncSession)->User:
    try:
        query = select(User).where(User.id == user_id)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.info(f"v1/users/crud/crud.py:get_user_by_id - User found: {user_id}")
            raise ProcederException(
                procederException=ProcederCodeException.user_does_not_exist
            )
        return user
    except Exception as e:  
        logger.error(f"v1/users/crud/crud.py:get_user_by_id - Error getting user by id: {e}")
        raise ProcederException(
            procederException=ProcederCodeException.server_error
        ) from e
        

async def get_email(email:str,session:AsyncSession)->User:
    try:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.info(f"v1/users/crud/crud.py:get_email - User found: {email}")
            raise ProcederException(
                procederException=ProcederCodeException.user_does_not_exist
            )
        return user
    except Exception as e:
        logger.error(f"v1/users/crud/crud.py:get_email - Error getting user by email: {e}")
        raise ProcederException(
            procederException=ProcederCodeException.server_error
        ) from e
        

async def get_username(username: str, session: AsyncSession) -> User:
    try:
        query = select(User).where(User.username == username)
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            logger.info(f"v1/users/crud/crud.py:get_username - User found: {username}")
            raise ProcederException(
                procederException=ProcederCodeException.user_does_not_exist
            )
        return user
    except Exception as e:
        logger.error(f"v1/users/crud/crud.py:get_username - Error getting user by username: {e}")
        raise ProcederException(
            procederException=ProcederCodeException.server_error
        ) from e


async def password_hash(password:str):
    try:
        return  bcrypt.hash(password)
    except Exception as e:
        logger.error(f"v1/users/crud/crud.py:password_hash - Error hashing password: {e}")
        raise ProcederException(
            procederException=ProcederCodeException.server_error
        ) from e


async def user_login(password: str,username : str,session: AsyncSession) -> bool:
    user = await get_username(username=username,session=session)
    if not bcrypt.verify(password,user.password):
        raise ProcederException(
            procederException=ProcederCodeException.wrong_username_or_password
        )
    return user


async def create(session: AsyncSession, username: str, email : str, password: str, first_name : str=None, last_name : str = None, admin : bool = False,):
    try:
        password = await password_hash(password)
        user = User(username=username,password=password,email=email,is_admin=admin,first_name=first_name,last_name=last_name)
        session.add(user) 
        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        logger.error(f"v1/users/crud/crud.py:create - Error creating user: {e}")
        raise ProcederException(
            procederException=ProcederCodeException.server_error
        ) from e
     
     
async def create_new_user(session: AsyncSession, username: str, email: str, password: str,admin : bool,first_name : str, last_name : str) -> User:
    if await user_exists(username,email,session):
        raise ProcederException(
            procederException=ProcederCodeException.user_already_exists
        )
    return await create(session, username, email, password,first_name,last_name,admin)

async def create_admin(session: AsyncSession, username: str, email: str, password: str):
    if not await user_exists(username, email, session):
        return await create(session, username, email, password,admin=True)