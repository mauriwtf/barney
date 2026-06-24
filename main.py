from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import crud, schemas
from api.v1.auth import api_router
from db.database import get_db
from schemas import ProductoCreate
from utils import verify_password
from auths import crear_token
from deps.deps import get_current_user, require_admin
app = FastAPI()
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Bienvenido a fastPI!"}

productos = []  

@app.get("/productos", response_model=list[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return crud.obtener_productos(db)

@app.get("/productos/{id}", tags=["Productos"], summary="Ver detalle de un producto")
def obtener_descripcion_producto(id: int):
    if id < len(productos):
        producto_nombre = productos[id]
        return {
            "id": id,
            "descripcion": f"Este es el producto: {producto_nombre}",
            "nombre": producto_nombre
        }
    return {"error": "Producto no encontrado"}

@app.post("/productos", response_model=schemas.ProductoCreate, dependencies=[Depends(require_admin)])
def agregar_productos(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.crear_producto(db, producto)

@app.put("/productos/{id}", response_model=schemas.ProductoCreate)
def actualizar_producto(producto_id: int, datos: schemas.ProductoCreate, db: Session = Depends(get_db)):
    if not productos:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return productos

@app.delete("/productos/{id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.eliminar_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}

@app.get("/items/", description="Esta es una descripción detallada del endpoint")
async def read_items():
    return [{"item_id": "Foo"}]

@app.post("/categorias", response_model=schemas.CategoriaResponse, dependencies=[Depends(require_admin)])
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.crear_categoria(db, categoria)

@app.get("/categorias", response_model=list[schemas.CategoriaResponse])
def listar_categoria(db: Session = Depends(get_db)):
    return crud.obtener_categorias(db)

@app.put("/productos/{producto_id}")
def endpoint_actualizar_producto(producto_id: int, datos: ProductoCreate, db: Session = Depends(get_db)):
    producto = crud.actualizar_producto(db, producto_id, datos)
    if producto is None:
        raise HTTPException(status_code=404, detail="El producto no existe")
    return producto

# --- USUARIOS ---

@app.post("/usuarios", response_model=schemas.UsuarioResponse, status_code=201)
def registrar_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    try:
        db_usuario = crud.obtener_usuario_por_email(db, email=usuario.email)
        if db_usuario:
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        
        nuevo_usuario = crud.crear_usuario(db=db, usuario=usuario)
        return nuevo_usuario

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.obtener_usuario_por_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas")
    token = crear_token(sub=user.email, es_admin=user.es_admin)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/usuarios/me", response_model=schemas.UsuarioResponse)
def leer_perfil(current_user = Depends(get_current_user)):
    return current_user

@app.get("/admin/ping")
def admin_ping(_admin = Depends(require_admin)):
    return {"ok": True, "role": "admin"}