from app.proceder.v1.users.schemas.schemas import CreateUser
from sqlmodel import Field
import uuid
from datetime import datetime
from typing import Optional

class ProcederUsers(CreateUser, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, title="User UUID")
    is_active: bool = Field(default=True, title="Is Active", description="Indicates if the user account is active")
    last_login: Optional[datetime] = Field(default_factory=datetime.now, title="Last Login", description="Timestamp when the user last logged in")
    is_admin: bool = Field(default=False, title="Is Admin", description="Indicates if the user has admin privileges")
    created_at: Optional[datetime] = Field(default_factory=datetime.now, title="Creation Timestamp", description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, title="Update Timestamp", description="Timestamp when the user was last updated")