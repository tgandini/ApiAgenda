from fastapi import FastAPI
from sqlalchemy.orm import Session
from bbdd import engine
from Routers import Auth, Persona, Contacto, Multiprocesamiento

tags_metadata = [
    {
        "name": "Personas",
        "description": "CRUD de personas"
    },
    {
        "name": "Contacto",
        "description": "CRUD de tanto teléfonos como direcciones"
    },
    {
        "name": "Pruebas de Concurrencia",
        "description": "Para medir tiempos de procesamiento linealmente, multiprocessing y multithreading"
    }
]

app = FastAPI(openapi_tags=tags_metadata)
app.include_router(Auth.router)
app.include_router(Persona.router)
app.include_router(Contacto.router)
app.include_router(Multiprocesamiento.router)