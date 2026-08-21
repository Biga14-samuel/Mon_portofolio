import secrets
from datetime import datetime, timedelta, timezone
from time import monotonic

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import Settings, get_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
bearer_scheme = HTTPBearer(auto_error=False)
failed_attempts: dict[str, list[float]] = {}


def get_client_ip(request: Request) -> str:
    # Always take the right-most IP to prevent spoofing by the client
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        ips = [ip.strip() for ip in forwarded_for.split(",")]
        if ips and ips[-1]:
            return ips[-1]

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        real_ip = real_ip.strip()
        if real_ip:
            return real_ip

    return request.client.host if request.client else "unknown"


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(subject: str, settings: Settings) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": subject, "exp": expires_at}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def check_rate_limit(request: Request) -> None:
    key = get_client_ip(request)
    now = monotonic()
    window_start = now - 60
    attempts = [timestamp for timestamp in failed_attempts.get(key, []) if timestamp >= window_start]
    failed_attempts[key] = attempts
    if len(attempts) >= 5:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Trop de tentatives. Reessayez dans une minute.",
        )


def register_failed_attempt(request: Request) -> None:
    key = get_client_ip(request)
    failed_attempts.setdefault(key, []).append(monotonic())


def clear_failed_attempts(request: Request) -> None:
    key = get_client_ip(request)
    failed_attempts.pop(key, None)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_settings),
) -> str:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentification requise.")

    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=["HS256"])
        username = payload.get("sub")
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide ou expire.") from exc

    if not username or not secrets.compare_digest(username, settings.admin_username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acces refuse.")

    return username
