from database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)

    productos = relationship(
        "Producto",
        back_populates="categorias"
    )

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)

    categorias = relationship(
        "Categoria",
        back_populates="productos"
    )