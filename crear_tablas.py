from db.database import engine, Base , hash_password , usuario , UsuarioCreate
from models import *
from sqlalchemy.orm import Session
from sqlalchemy import or_

Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente")


def obtener_usuario_por_mail(db:Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email).first()

def obtener_usuario_por_id(db:Session, usuario_id: int ) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.id == usuario.id). first()

def crear_usuario(db:Session, usuario: UsuarioCreate) -> Usuario:
    existe = db.query(usuario).filter(
        or_(Usuario.email == usuario.email, Usuario.nombre == usuario.nombre)
    ).first()
    if existe:
        raise ValueError("Ya existe un usuario con ese email o nombre")
    
    db_usuario = Usuario(
        nombre = usuario.nombre,
        email = usuario.email,
        hash_password = hash_password(usuario.password),
        es_admin = usuario.es_admin
    )

    db.add(db.usuario)
    db.commit()
    db.refresh(db.usuario)
    return db_usuario