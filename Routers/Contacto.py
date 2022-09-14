from fastapi import APIRouter
from pydantic import BaseModel
from Models.Persona import Persona
from Models.Contacto import Contacto
from bbdd import engine
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/contacto",
    tags=["Contacto"]
)

class contactoJson (BaseModel):
    idPersona: int
    valor: str

#add telefono a persona por idpersona ingresados por json
@router.put("/agregarTelefono")
async def agregar_telefono(contacto: contactoJson):
    try:
        with Session(engine) as sesion:            
            personaDB = sesion.query(Persona).filter(Persona.id == contacto.idPersona).first()
            if personaDB is None:
                return {"message": "No se ha encontrado la persona"}
            else:
                contactoDB = Contacto(tipoContacto="Telefono", valor=contacto.valor)
                personaDB.contactos.append(contactoDB)
                sesion.commit()
                sesion.refresh(personaDB)

                return {"message": "Telefono agregado a la persona",
                        "id": personaDB.id,
                        "nombre": personaDB.nombre,
                        "apellido": personaDB.apellido,
                        "contactos": [{"tipoContacto": contactoDB.tipoContacto,
                                        "valor": contactoDB.valor} for contactoDB in personaDB.contactos]
                        }
    except Exception as e:
        return {"error" : str(e)}

@router.put("/agregarDireccion")
async def agregar_direccion(contacto: contactoJson):
    try:
        with Session(engine) as sesion:            
            personaDB = sesion.query(Persona).filter(Persona.id == contacto.idPersona).first()
            if personaDB is None:
                return {"message": "No se ha encontrado la persona"}
            else:
                contactoDB = Contacto(tipoContacto="Direccion", valor=contacto.valor)
                personaDB.contactos.append(contactoDB)
                sesion.commit()
                sesion.refresh(personaDB)

                return {"message": "Direccion agregada a la persona",
                        "id": personaDB.id,
                        "nombre": personaDB.nombre,
                        "apellido": personaDB.apellido,
                        "contactos": [{"tipoContacto": contactoDB.tipoContacto,
                                        "valor": contactoDB.valor} for contactoDB in personaDB.contactos]
                        }
    except Exception as e:
        return {"error" : str(e)}

@router.delete("/{idContacto}")
async def eliminar_contacto(idContacto: int):
    try:
        with Session(engine) as sesion:
            contactoDB = sesion.query(Contacto).filter(Contacto.id == idContacto).first()
            if contactoDB is None:
                return {"message": "No se ha encontrado el contacto"}
            else:
                sesion.delete(contactoDB)
                sesion.commit()
                return {"message": "Contacto eliminado"}
    except Exception as e:
        return {"error" : str(e)}
