from jose import jwt, JWTError
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.settings import settings

from config.settings import settings
from contextvars import ContextVar

user_context: ContextVar[str] = ContextVar("user_context", default=None)

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
SECRET_KEY = settings.secret_key
REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


def get_user_id_from_token(jwtoken: str):
    try:
        payload = jwt.decode(jwtoken, SECRET_KEY, ALGORITHM)
        user_id = payload.get("sub")
    except JWTError:
        user_id = None
    return user_id


def decodeJWT(jwtoken: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, SECRET_KEY, ALGORITHM)
        return payload
    except JWTError:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=401, detail="Invalid token or expired token."
                )
            user_id = get_user_id_from_token(credentials.credentials)
            user_context.set(user_id)
            return credentials.credentials
        else:
            raise HTTPException(status_code=401, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


jwt_bearer = JWTBearer()
