from sqlalchemy.ext.asyncio import AsyncSession
from app.proceder.v1.users.models.models import ProcederUsers as User
from sqlalchemy.future import select
from fastapi import HTTPException, status
from passlib.hash import bcrypt


def __user_does_not_exist()->HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Username does not exist"
    )
    

async def user_exists(username:str,email:str,session:AsyncSession) -> None:
    query = select(User).where((User.username == username) | (User.email == email))
    result = await session.execute(query)
    return result.scalars().first()



async def get_user_by_id(user_id:str,session:AsyncSession)->User:
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        raise __user_does_not_exist()
    return user


async def get_email(email:str,session:AsyncSession)->User:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        raise __user_does_not_exist()
    return user


async def get_username(username: str, session: AsyncSession) -> User:
    query = select(User).where(User.username == username)
    result = await session.execute(query)
    user = result.scalars().first()
    if not user:
        raise __user_does_not_exist()
    return user


async def password_hash(password:str):
    return  bcrypt.hash(password)


async def user_login(password: str,username : str,session: AsyncSession) -> bool:
    user = await get_username(username=username,session=session)
    if not bcrypt.verify(password,user.password):
        raise HTTPException(status_code=400,detail="wrong username or password")
    return user

async def create(session: AsyncSession, username: str, email : str, password: str, first_name : str=None, last_name : str = None, admin : bool = False,):
    password = await password_hash(password)
    user = User(username=username,password=password,email=email,is_admin=admin,first_name=first_name,last_name=last_name)
    session.add(user) 
    await session.commit()
    await session.refresh(user)
    return user
    
async def create_new_user(session: AsyncSession, username: str, email: str, password: str,admin : bool,first_name : str, last_name : str) -> User:
    if await user_exists(username,email,session):
        raise HTTPException(status_code=400, detail="Username or email already registered")
    return await create(session, username, email, password,first_name,last_name,admin)

async def create_admin(session: AsyncSession, username: str, email: str, password: str):
    if not await user_exists(username, email, session):
        return await create(session, username, email, password,admin=True)