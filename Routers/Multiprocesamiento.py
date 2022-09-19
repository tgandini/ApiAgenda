from turtle import title
from fastapi import APIRouter
from sqlalchemy.orm import Session
from bbdd import engine
from time import time
from faker import Faker
from multiprocessing import Process, Manager
from threading import Thread


def instanciar_personas_aleatorias(lista_personas_instanciadas: list, cantidad_Registros: int, un_solo_guardado: bool = True):
    from Models.Persona import Persona as persona_db
    fake = Faker('es_ES')
    lista_usuarios_para_guardar_ahora = []
    for i in range(cantidad_Registros):
        persona_instanciada = persona_db(
            nombre=fake.first_name(), apellido=fake.last_name())
        # Si se guarda solo al final, lo agregamos a la lista de personas para agregar al final. Si no se guarda solo al final, lo agregamos a una lista para guardar ahora
        if un_solo_guardado:
            lista_personas_instanciadas.append(persona_instanciada)
        else:
            lista_usuarios_para_guardar_ahora.append(persona_instanciada)
    # Si NO hay un solo guardado, tenemos que persistir ahora la lista generada en este proceso
    if not un_solo_guardado:
        with Session(engine) as sesion:
            sesion.add_all(lista_usuarios_para_guardar_ahora)
            sesion.commit()


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


@router.post("/multiproceso/{cantidad_registros}/{cantidad_procesos}/{un_solo_guardado}")
async def insertar_multiproceso(cantidad_registros: int, cantidad_procesos: int, un_solo_guardado: bool = True):

    lista_personas_instanciadas = Manager().list()
    lista_procesos = []
    tiempo_inicio = time()

    for c in range(cantidad_procesos):
        unProceso = Process(target=instanciar_personas_aleatorias, args=(
            lista_personas_instanciadas, cantidad_registros//cantidad_procesos, un_solo_guardado))
        lista_procesos.append(unProceso)
    # iniciamos procesos
    for proceso in lista_procesos:
        proceso.start()
    # sincronizamos procesos
    for proceso in lista_procesos:
        proceso.join()

    # si es 1 solo guardado, guardamos acá en la BBDD la lista de personas instanciadas
    if un_solo_guardado:
        with Session(engine) as sesion:
            sesion.add_all(list(lista_personas_instanciadas))
            sesion.commit()
    tiempo_fin = time()

    duracion = tiempo_fin - tiempo_inicio
    return {"tipo": "multiproceso", "duracion": str(round(duracion, 2))+" segundos"}


@router.post("/multithreading/{cantidad_registros}/{cantidad_hilos}/{un_solo_guardado}")
async def insertar_multithreading(cantidad_registros: int, cantidad_hilos: int, un_solo_guardado: bool = True):
    lista_personas_instanciadas = []
    lista_hilos = []
    tiempo_inicio = time()

    for c in range(cantidad_hilos):
        un_hilo = Thread(target=instanciar_personas_aleatorias, args=(
            lista_personas_instanciadas, cantidad_registros//cantidad_hilos, un_solo_guardado))
        lista_hilos.append(un_hilo)

    # iniciamos hilos
    for hilo in lista_hilos:
        hilo.start()
    # sincronizamos hilos
    for hilo in lista_hilos:
        hilo.join()

    # guardamos en la BBDD la lista de personas instanciadas
    if un_solo_guardado:
        with Session(engine) as sesion:
            sesion.add_all(list(lista_personas_instanciadas))
            sesion.commit()
    tiempo_fin = time()

    duracion = tiempo_fin - tiempo_inicio
    return {"tipo": "multithreading", "duracion": str(round(duracion, 2))+" segundos"}
