from sqlmodel import SQLModel, Field
import uuid
from typing import Optional
from pydantic import EmailStr


class Base(SQLModel):
    username: str = Field(..., title="Username", max_length=50)
    password: str = Field(..., title="Password", min_length=8)


class CreateUser(Base):
    first_name: Optional[str] = Field(None, title="First Name", max_length=50)
    last_name: Optional[str] = Field(None, title="Last Name", max_length=50)
    email: EmailStr = Field(..., title="Email", max_length=100)


class UserResponse(SQLModel):
    id: uuid.UUID
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


class UserLogin(SQLModel):
    username: str
    password: str


class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str


class TokenVerifyResponse(SQLModel):
    token: bool
