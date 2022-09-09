from bbdd import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Contacto(Base):
    __tablename__ = 'contactos'
    id = Column(Integer, primary_key=True)
    tipoContacto = Column(String(50), nullable=False)
    valor = Column(String(50), nullable=False)
    personas = relationship("Persona", secondary="association", back_populates="contactos")     