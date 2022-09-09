from bbdd import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

tablaContactosPersonas = Table(
    "personas_contactos",
    Base.metadata,
    Column("persona_id", ForeignKey("personas.id"), primary_key=True),
    Column("contacto_id", ForeignKey("contactos.id"), primary_key=True),
)

class Persona(Base):
    __tablename__ = 'personas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    contactos = relationship("Contacto", secondary=tablaContactosPersonas, back_populates="personas")
    