from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.auth_handler import decode_jwt
from app.logger import logger

class JWTBearer(HTTPBearer):
    def __init__(self, token_types: list[str] = ["access"], auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.token_types = token_types
        self.access_cookie_name = "access_token"
        self.refresh_cookie_name = "refresh_token"

    async def __call__(self, request: Request):
        # 1. Tenta autenticar via Header
        header_token = await self._get_token_from_header(request)
        if header_token:
            logger.info("Token found in Authorization header")
            if self._verify_jwt(header_token):
                logger.info("Authorization header token successfully validated")
                return header_token
            logger.warning("Invalid or expired token in Authorization header")
        
        logger.debug("Checking cookies for tokens")
        
        # 2. Tenta autenticar via Cookies
        access_token = request.cookies.get(self.access_cookie_name)
        refresh_token = request.cookies.get(self.refresh_cookie_name)

        if access_token and self._verify_jwt(access_token):
            logger.info("Access token from cookies successfully validated")
            return access_token

        if refresh_token and self._verify_jwt(refresh_token):
            logger.info("Access token expired, but refresh token from cookies is valid")
            return refresh_token

        logger.warning("No valid token found in header or cookies")
        raise HTTPException(status_code=403, detail="Not authenticated")

    async def _get_token_from_header(self, request: Request) -> str | None:
        try:
            credentials: HTTPAuthorizationCredentials = await super().__call__(request)
            if credentials and credentials.scheme == "Bearer":
                return credentials.credentials
        except Exception as e:
            logger.debug(f"Error parsing Authorization header: {e}")
        return None

    def _verify_jwt(self, jwtoken: str | None) -> bool:
        if not jwtoken:
            return False
        try:
            payload = decode_jwt(jwtoken)
            if not payload:
                logger.debug("Decoded JWT returned empty payload")
                return False
            token_type = payload.get("type")
            if token_type not in self.token_types:
                logger.debug(f"Token type '{token_type}' not allowed. Allowed types: {self.token_types}")
                return False
            logger.info(f"JWT payload: {payload}")
            return True
        except Exception as e:
            logger.error(f"JWT verification failed: {e}")
            return False
