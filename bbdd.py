from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()
from Models import Persona, Contacto
engine = create_engine('postgresql://admin:admin@localhost:5432/ApiAgenda')
Base.metadata.create_all(engine)