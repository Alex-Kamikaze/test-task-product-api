import logging
import uuid

from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.models import *
from security import PasswordSecurity


app = FastAPI()
logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


@app.exception_handler(Exception)
async def handle_exception(req: Request, exc: Exception):
    logger.error(str(exc))


@app.post("/token")
async def handle_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_info = session.query(User).filter_by(user_login = form_data.username).first()
    if user_info is None:
        raise HTTPException(400, details = f"Пользователя с логином {form_data.username} не существует!")
    
    if not PasswordSecurity.check_password_hash(form_data.password, user_info.user_password):
        raise HTTPException(400, details = "Неверный логин или пароль")

    return { "access_token": uuid.uuid4().hex}

    
