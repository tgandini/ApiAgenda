from bbdd import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Contacto(Base):
    __tablename__ = 'contactos'
    id = Column(Integer, primary_key=True)
    tipoContacto = Column(String(50), nullable=False)
    valor = Column(String(50), nullable=False)
    persona_id = Column(Integer, ForeignKey('personas.id'))
    persona = relationship("Persona", back_populates="contactos")

    def crearTelefono(self, valor):
        self.tipoContacto = "Telefono"
        self.valor = valor
    
    def crearDireccion(self, valor):
        self.tipoContacto = "Direccion"
        self.valor = valor

    def __repr__(self):
        return f"{self.tipoContacto}: {self.valor}"
