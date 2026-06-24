from fastapi import APIRouter

from fastapi import Depends
from sqlalchemy.orm import Session

from schemas import CategoriaResponse, CategoriaCreate
from deps.deps import get_db

from crud import crear_categoria, obtener_categoria

api_router = APIRouter()


@api_router.post("/", response_model=CategoriaResponse)
def crear_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return crear_categoria(db, categoria)


@api_router.get("/", response_model=list[CategoriaResponse])
def listar_categoria(db: Session = Depends(get_db)):
    return obtener_categoria(db)