from fastapi import FastAPI
import bbdd


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

#saludar con nombre y apellido
@app.get("/saludar/{nombre}/{apellido}")
async def saludar(nombre: str, apellido: str):
    return {"message": f"Hola {nombre} {apellido}!! ¿Cómo estás?"}