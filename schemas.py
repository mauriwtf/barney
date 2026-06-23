from pydantic import BaseModel,EmailStr





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




#usuario


class UsuarioBase(BaseModel):
    nomre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    password:str
    es_admin: bool=False

class UsuarioResponse(UsuarioBase):
    id: int
    es_admin: bool

    class config:
        orm_mode = True

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    password: str
    es_admin: bool = False


class UsuarioResponse(UsuarioBase):
    id: int
    es_admin: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"