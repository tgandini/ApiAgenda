from fastapi import FastAPI
from sqlalchemy.orm import Session
from bbdd import engine
from Routers import Persona, Contacto

tags_metadata = [
    {
        "name": "Personas",
        "description": "CRUD de personas"
    },
    {
        "name": "Contacto",
        "description": "CRUD de tanto teléfonos como direcciones"
    }
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(Persona.router)
app.include_router(Contacto.router)