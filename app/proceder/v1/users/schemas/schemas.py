from sqlmodel import SQLModel, Field
import uuid
from typing import Optional

class CreateUser(SQLModel):
    first_name: Optional[str] = Field(..., title="First Name", max_length=50)
    last_name: Optional[str] = Field(..., title="Last Name", max_length=50)
    username: str = Field(..., title="Username", max_length=50)
    password: str = Field(..., title="Password", min_length=8)
    email: str = Field(..., title="Email", max_length=100)

class UserResponse(SQLModel):
    id:uuid.UUID
    username: str
    email: str

class UserLogin(SQLModel):
    username: str
    password: str

class TokenResponse(SQLModel):
    access_token: str
    refresh_token: str


class TokenVerifyResponse(SQLModel):
    token:bool