from fastapi import FastAPI
import bbdd
from sqlalchemy.orm import Session
from bbdd import engine
from pydantic import BaseModel


app = FastAPI()

class personaJson (BaseModel):
    nombre: str
    apellido: str
class contactoJson (BaseModel):
    idPersona: int
    valor: str


@app.get("/")
async def getAllPersonas():
    try:
        session = Session(bind=engine)
        from Models.Persona import Persona
        personas = session.query(Persona).all()
        session.close()
        return personas
    except Exception as e:
        return {"error": str(e)}


@app.put("/persona")
async def crearPersona(persona: personaJson):
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
@app.get("/persona/{nombreOApellido}")
async def getPersona(nombreOApellido):
    try:
        with Session(engine) as sesion:
            from Models.Persona import Persona
            #find all personas with nombre or apellido like nombreOApellido case insensitive
            personasDB = sesion.query(Persona).filter(Persona.nombre.ilike(f"%{nombreOApellido}%") | Persona.apellido.ilike(f"%{nombreOApellido}%")).all()

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

#add telefono a persona por idpersona ingresados por json
@app.put("/agregarTelefono")
async def agregarTelefono(contacto: contactoJson):
    try:
        with Session(engine) as sesion:
            from Models.Persona import Persona
            from Models.Contacto import Contacto
            
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

@app.put("/agregarDireccion")
async def agregarDireccion(contacto: contactoJson):
    try:
        with Session(engine) as sesion:
            from Models.Persona import Persona
            from Models.Contacto import Contacto
            
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

@app.delete("/eliminarContacto/{idContacto}")
async def eliminarContacto(idContacto: int):
    try:
        with Session(engine) as sesion:
            from Models.Contacto import Contacto
            
            contactoDB = sesion.query(Contacto).filter(Contacto.id == idContacto).first()
            if contactoDB is None:
                return {"message": "No se ha encontrado el contacto"}
            else:
                sesion.delete(contactoDB)
                sesion.commit()
                return {"message": "Contacto eliminado"}
    except Exception as e:
        return {"error" : str(e)}

@app.delete("/eliminarPersona/{idPersona}")
async def eliminarPersona(idPersona: int):
    try:
        with Session(engine) as sesion:
            from Models.Persona import Persona
            
            personaDB = sesion.query(Persona).filter(Persona.id == idPersona).first()
            if personaDB is None:
                return {"message": "No se ha encontrado la persona"}
            else:
                sesion.delete(personaDB)
                sesion.commit()
                return {"message": "Persona eliminada"}
    except Exception as e:
        return {"error" : str(e)}