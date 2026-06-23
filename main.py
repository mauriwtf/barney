from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud, schemas
from db.database import get_db

from fastapi.security import OAuth2PasswordRequestForm
from utils import verify_password
from auths import crear_token
from deps import get_current_user, require_admin

app= FastAPI()


app.include_router(api_router, prefix="api/v1")

@app.get("/productos", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.obtener_productos(db)

@app.post(
    "/productos",
    response_model=schemas.ProductoCreate,
    dependencies=[Depends(require_admin)]
)
def agregar_producto(
    producto: schemas.ProductoCreate,
    db: Session = Depends(get_db)
):
    return crud.crear_producto(db, producto)

@app.put("/productos/{id}", response_model=schemas.ProductoCreate)
def actualizar_producto(
    producto_id: int,
    datos: schemas.ProductoCreate,
    db: Session = Depends(get_db)
):
    producto = crud.actualizar_producto(db, producto_id, datos)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto

@app.delete("/productos/{id}")
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(get_db)
):
    producto = crud.eliminar_producto(db, producto_id)

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return {"mensaje": "Producto eliminado"}

### Usuarios

@app.post(
    "/usuarios",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_usuario(
    usuario: schemas.UsuarioCreate,
    db: Session = Depends(get_db)
):
    try:
        return crud.crear_usuario(db, usuario)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.obtener_usuario_por_email(
        db,
        form_data.username
    )

    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales invalidas"
        )

    token = crear_token(
        {
            "sub": user.email,
            "es_admin": user.es_admin
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get(
    "/usuarios/me",
    response_model=schemas.UsuarioResponse
)
def leer_perfil(
    current_user = Depends(get_current_user)
):
    return current_user

@app.get("/admin/ping")
def admin_ping(
    admin = Depends(require_admin)
):
    return {
        "ok": True,
        "role": "admin"
    }