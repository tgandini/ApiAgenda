from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from globals import urlBBDD

Base = declarative_base()
from Models import *
engine = create_engine(urlBBDD)
Base.metadata.create_all(engine)