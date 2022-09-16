from turtle import title
from fastapi import APIRouter
from sqlalchemy.orm import Session
from bbdd import engine
from time import time
from faker import Faker
from multiprocessing import Process, Manager
from threading import Thread


def instanciar_personas_aleatorias(lista_personas_instanciadas: list, cantidad_Registros: int):
    from Models.Persona import Persona as persona_db
    fake = Faker('es_ES')
    for i in range(cantidad_Registros):
        lista_personas_instanciadas.append(
            persona_db(nombre=fake.first_name(), apellido=fake.last_name()))


router = APIRouter(
    prefix="/concu",
    tags=["Pruebas de Concurrencia"]
)

@router.post("/lineal/{cantidad_registros}")
async def insertar_lineal(cantidad_registros: int):
    tiempo_inicio = time()
    lista_personas_instanciadas = []
    instanciar_personas_aleatorias(
        lista_personas_instanciadas, cantidad_registros)
    with Session(engine) as sesion:
        sesion.add_all(lista_personas_instanciadas)
        sesion.commit()
    tiempo_fin = time()

    duracion = tiempo_fin - tiempo_inicio
    return {"tipo": "lineal", "duracion": str(round(duracion, 2))+" segundos"}

@router.post("/multiproceso/{cantidad_registros}/{cantidad_procesos}")
async def insertar_multiproceso(cantidad_registros: int, cantidad_procesos: int):
       
    lista_personas_instanciadas = Manager().list()
    lista_procesos = []
    tiempo_inicio = time()

    for c in range(cantidad_procesos):
        unProceso = Process(target=instanciar_personas_aleatorias, args=(
            lista_personas_instanciadas, cantidad_registros//cantidad_procesos))
        lista_procesos.append(unProceso)

    #iniciamos procesos
    for proceso in lista_procesos:
        proceso.start()
    # sincronizamos procesos
    for proceso in lista_procesos:
        proceso.join()

    #guardamos en la BBDD la lista de personas instanciadas
    with Session(engine) as sesion:
        sesion.add_all(list(lista_personas_instanciadas))
        sesion.commit()
    tiempo_fin = time()

    duracion = tiempo_fin - tiempo_inicio
    return {"tipo": "multiproceso", "duracion": str(round(duracion, 2))+" segundos"}

@router.post("/multithreading/{cantidad_registros}/{cantidad_hilos}")
async def insertar_multithreading(cantidad_registros: int, cantidad_hilos: int):
    lista_personas_instanciadas = []
    lista_hilos = []
    tiempo_inicio = time()

    for c in range(cantidad_hilos):
        un_hilo = Thread(target=instanciar_personas_aleatorias, args=(
            lista_personas_instanciadas, cantidad_registros//cantidad_hilos))
        lista_hilos.append(un_hilo)

    #iniciamos hilos
    for hilo in lista_hilos:
        hilo.start()
    # sincronizamos hilos
    for hilo in lista_hilos:
        hilo.join()

    #guardamos en la BBDD la lista de personas instanciadas
    with Session(engine) as sesion:
        sesion.add_all(list(lista_personas_instanciadas))
        sesion.commit()
    tiempo_fin = time()

    duracion = tiempo_fin - tiempo_inicio
    return {"tipo": "multithreading", "duracion": str(round(duracion, 2))+" segundos"}
