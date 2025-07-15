from fastapi import HTTPException,status
from dataclasses import dataclass
from enum import Enum

@dataclass
class ProcederExceptionDetail:
    detail: str
    code: int
    http_response: str

class ProcederCodeException():
    server_error = ProcederExceptionDetail(
        detail="Internal Server Error",
        code="P5000",
        http_response=status.HTTP_500_INTERNAL_SERVER_ERROR
    )
    
    user_already_exists = ProcederExceptionDetail(
        detail="UserName or email already exists",
        code="P4444",
        http_response=status.HTTP_400_BAD_REQUEST
    )
    
    user_not_found = ProcederExceptionDetail(
        detail="User not found",
        code="P4004",
        http_response=status.HTTP_404_NOT_FOUND
    )
    
    user_does_not_exist = ProcederExceptionDetail(
        detail="User does not exist",
        code="P4404",
        http_response=status.HTTP_404_NOT_FOUND
    )
    
    wrong_username_or_password = ProcederExceptionDetail(
        detail="Wrong username or password",
        code="P4001",
        http_response=status.HTTP_401_UNAUTHORIZED
    )

class ProcederException(HTTPException):
    def __init__(self, procederException: ProcederExceptionDetail):
        super().__init__(
            status_code=procederException.http_response,
            detail={
                "code": procederException.code,
                "message": procederException.detail
            }
        )
        