from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import crud, schemas
from db.database import get_db
from schemas import ProductoCreate
from utils import verify_password
from auths import crear_token
import api
from deps.deps import get_current_user, require_admin
api_router = APIRouter()

@api_router.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_usuario(db, usuario)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@api_router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.obtener_usuario_por_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    token = crear_token(sub=user.email, es_admin=user.es_admin)
    return {"access_token": token, "token_type": "bearer"}


@api_router.get("/usuarios/me", response_model=schemas.UsuarioResponse)
def leer_perfil(current_user = Depends(get_current_user)):
    return current_user


@api_router.get("/admin/ping")
def admin_ping(_admin = Depends(require_admin)):
    return {"ok": True, "role": "admin"}