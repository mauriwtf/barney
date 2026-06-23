from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
SECRET_KEY = "mauri420238"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def crear_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verificar_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload

    except JWTError:
        return None

def crear_token(sub: str, es_admin: bool):
    to_encode = {
        "sub": sub,
        "es_admin": es_admin
    }

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def crear_token(sub:str, es_admin:bool):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": sub,
        "exp": expire,
        "es_admin": es_admin
    }

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def crear_token(sub:str, es_admin:bool):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": sub,
        "exp": expire,
        "es_admin": es_admin
    }

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verificar_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
