from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from globals import conStringBBDD

Base = declarative_base()
from Models import Persona, Contacto

engine = create_engine(conStringBBDD)
Base.metadata.create_all(engine)