from turtle import title
from fastapi import APIRouter
from sqlalchemy.orm import Session
from bbdd import engine
from Models.Persona import Persona as PersonaDB
from pydantic import BaseModel
from fastapi import Depends
from .Auth import checkear_logueo


router = APIRouter(
    prefix="/personas",
    tags=["Personas"]
)

class personaJson (BaseModel):
    nombre: str
    apellido: str

@router.get("/")
async def get_todas_las_personas(user: str = Depends(checkear_logueo)):
    usuarioLogueado= user
    try:
        session = Session(bind=engine)
        personas = session.query(PersonaDB).filter(PersonaDB.estaOculto == False).all()
        session.close()
        return personas
    except Exception as e:
        
        return {"error": str(e)}

@router.put("/")
async def crear_persona(persona: personaJson, user: str = Depends(checkear_logueo)):
    try:
        with Session(engine) as sesion:
            from Models.Persona import Persona
            persona.nombre = persona.nombre.title()
            persona.apellido = persona.apellido.title()
            personaDB = Persona(nombre=persona.nombre, apellido=persona.apellido)
            sesion.add(personaDB)            
            sesion.commit()
            sesion.refresh(personaDB)

            return {"message": "Persona creada con éxito",
                    "id": personaDB.id,
                    "nombre": personaDB.nombre,
                    "apellido": personaDB.apellido
                    }
    except Exception as e:
        return {"error" : str(e)}

#get personas por nombre o apellido
@router.get("/{nombreOApellido}")
async def get_persona(nombreOApellido, user: str = Depends(checkear_logueo)):
    try:
        with Session(engine) as sesion:
            from Models.Persona import Persona
            personasDB = sesion.query(Persona).filter(Persona.estaOculto == False).filter((Persona.nombre.ilike(f"%{nombreOApellido}%")) | (Persona.apellido.ilike(f"%{nombreOApellido}%"))).all()

            if len(personasDB) == 0:
                return {"message": "No se han encontrado personas con ese nombre y apellido"}
            else:
                return {"message": "Se han encontrado personas",
                        "personas" : [{"id": personaEnBBDD.id,
                                        "nombre": personaEnBBDD.nombre,
                                        "apellido": personaEnBBDD.apellido,
                                        "contactos": [{
                                            "idContacto": contactoDB.id,
                                            "tipoContacto": contactoDB.tipoContacto,
                                            "valor": contactoDB.valor} for contactoDB in personaEnBBDD.contactos]
                                        } for personaEnBBDD in personasDB]                                        
                        }
    except Exception as e:
        return {"error" : str(e)}

@router.delete("/{idPersona}")
async def eliminar_persona(idPersona: int, user: str = Depends(checkear_logueo)):
    try:
        with Session(engine) as sesion:
            personaDB = sesion.query(PersonaDB).filter(PersonaDB.id == idPersona).first()
            if personaDB is None:
                return {"message": "No se ha encontrado la persona"}
            else:
                sesion.delete(personaDB)
                sesion.commit()
                return {"message": "Persona eliminada"}
    except Exception as e:
        return {"error" : str(e)}