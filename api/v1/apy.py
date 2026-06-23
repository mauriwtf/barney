from fastapi import APIRouter


api_router= APIRouter()

api_router.include_router(auth.routher, prefix="/auth" tags=["auth"])
api_router.include_router(productos.routher, prefix="/productos" tags=["productos"])
api_router.include_router(categorias.routher, prefix="/categorias" tags=["categorias"])
