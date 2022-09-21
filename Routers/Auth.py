from fastapi import Depends, FastAPI, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from jose import jwt



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    prefix="/auth"
)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if password!="admin":
        raise HTTPException(status_code=401, detail="Logueo incorrecto")

    #creamos el token a devolver
    encodear = {"username": username, "exp": (datetime.utcnow() + timedelta(minutes=5)).timestamp()}
    jwt_encoded = jwt.encode(encodear, "abracadabra", algorithm="HS256")
    return {"access_token": jwt_encoded, "token_type": "bearer"}

#checkear validez y vigencia del token
def checkear_logueo(token = Depends(oauth2_scheme)):

    payload = jwt.decode(token, "abracadabra", algorithms=["HS256"])
    username = payload.get("username")
    exp = payload.get("exp")
    if username is None:
        raise HTTPException(status_code=401, detail="Token invalido")
    if exp is None or exp < datetime.utcnow().timestamp():
        raise HTTPException(status_code=401, detail="Token expirado")
    return username
    