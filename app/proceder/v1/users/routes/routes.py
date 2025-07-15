
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_session
from app.proceder.v1.users.schemas.schemas import UserLogin, CreateUser, UserResponse, TokenResponse, TokenVerifyResponse
from app.auth.auth_handler import sign_jwt
from app.auth.auth_bearer import JWTBearer
from app.proceder.v1.users.crud.crud import create_new_user,get_email,get_username,user_login
from app.middleware.rate_limit import limiter   
from app.config.settings import secrets, envirinment    
from app.proceder.v1.users.exceptions.exceptions import ProcederException, ProcederExceptionDetail


router = APIRouter()

@router.post('/login', response_model=TokenResponse, tags=['users'])
@limiter.limit("5/minute")
async def login(user: UserLogin, request: Request, response: Response, session: AsyncSession = Depends(get_session)):
    try:
        user = await user_login(username=user.username, session=session, password=user.password)

        access_token = sign_jwt(
            user.id,
            expires=600, # 10min
            token_type="access"
        )

        refresh_token = sign_jwt(
            user.id,
            expires=3600 * 24 * 7,  # 7 dias, por exemplo
            token_type="refresh"
        )

        # Armazenar o access token como cookie seguro
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=True if envirinment == 'prod' else False,
            samesite="Lax"
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True,
            secure=True if envirinment == 'prod' else False,
            samesite="Lax"
        )

        return TokenResponse(access_token=access_token,refresh_token=refresh_token)

    except HTTPException as e:
        raise ProcedureException(
            detail=str(e.detail),
            status_code=e.status_code
        )

    
@router.get("/verify",
            dependencies=[Depends(JWTBearer())],
            response_model=TokenVerifyResponse,
            tags=['users'],
)
async def verify_token(request: Request,response: Response):
    return TokenVerifyResponse(token=True)


@router.post("/create", response_model=UserResponse,tags=['users'],dependencies=[Depends(JWTBearer())],)
@limiter.limit("1/minute")
async def create_user(user_create: CreateUser,request: Request,response:Response, session: AsyncSession = Depends(get_session)):
    try:
        user = await create_new_user(
            session=session,
            admin=False,
            **user_create.dict()
        )
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


