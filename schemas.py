from pydantic import BaseModel





class ProductoCreate(BaseModel):
    nombre:str
    precio:float
    en_stock: bool
    categoria_id:int

class ProductoResponse(BaseModel):
    id:int
    class config:
        orm_mode = True

class CategoriaBase(BaseModel):
    nombre:str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id:int

    class config:
        orm_node= True