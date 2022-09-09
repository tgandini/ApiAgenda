from bbdd import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from Models import Contacto

class Persona(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    contactos = relationship("Contacto", back_populates="persona")

    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido
        self.contactos=[]

    def __repr__(self):
        return f"{self.nombre} {self.apellido}. Contactos: {self.contactos}"
        