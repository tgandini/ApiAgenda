from bbdd import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Persona(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    contactos = relationship("Contacto", back_populates="persona", cascade="all, delete-orphan")
    estaOculto = Column(Boolean, default=False, nullable=False)

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.contactos=[]
        self.estaOculto=False

    def __repr__(self):
        return f"{self.nombre} {self.apellido}. Contactos: {self.contactos}"
    
    def ocultar(self):
        self.estaOculto=True
    
    def mostrar(self):
        self.estaOculto=False      