from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from Config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def crear_token(sub:str, es_admin:bool):
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    data = {
        "sub": sub,
        "exp": expire,
        "es_admin": es_admin
    }

    token = jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token


def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        return payload

    except JWTError:
        return None


def hash_password(password:str):
    return pwd_context.hash(password)


def verify_password(password:str, hashed: str):
    return pwd_context.verify(password, hashed)