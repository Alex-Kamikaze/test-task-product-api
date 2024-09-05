import logging
import uuid

from typing import List

from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.models import *
from api.security import PasswordSecurity
from api.types import *


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
        raise HTTPException(400, detail = f"Пользователя с логином {form_data.username} не существует!")
    
    if not PasswordSecurity.check_password_hash(form_data.password, user_info.user_password):
        raise HTTPException(400, detail = "Неверный логин или пароль")

    return { "access_token": uuid.uuid4().hex}


@app.get("/categories/all")
async def get_all_categories() -> List[CategoryModel]:
    categories = session.query(Category).all()
    if categories is None:
        return []
    return [CategoryMapper.from_db_model(category) for category in categories]

@app.get("/products/all")
async def get_all_products() -> List[ProductModel]:
    products = session.query(Product).all()
    if products is None:
        return []
    
    return [ProductMapper.from_db_model(product) for product in products]

@app.post("/users/register")
async def register_new_user(user_info: UserRegistrationModel):
    if session.query(User).filter_by(user_login = user_info.user_login).first() is not None:
        raise HTTPException(400, detail = f"Пользователь с логином {user_info.user_login} уже существует!")
    user_hashed_password = PasswordSecurity.hash_password(user_info.user_password)
    new_user = User(user_login = user_info.user_login, user_password = user_hashed_password)
    session.add(new_user)
    session.commit()
    return { "status": "OK" }

@app.post("/products/add")
async def add_new_product(product: ProductModel, token: str = Depends(oauth2_scheme)):
    session.add(ProductMapper.into_db_model(product))
    session.commit()
    return { "status": "OK" }

@app.delete("/products/delete")
async def delete_product(product_id: int, token: str = Depends(oauth2_scheme)):
    product_to_delete = session.query(Product).filter_by(product_id=product_id).first()
    if product_to_delete is None:
        raise HTTPException(404, detail = f"Продукта с ID {product_id} не существует!")
    session.delete(product_to_delete)
    session.commit()
    return { "status": "OK" }

@app.delete("/categories/delete")
async def delete_category(category_id: int, token: str = Depends(oauth2_scheme)):
    category_to_delete = session.query(Category).filter_by(category_id=category_id).first()
    if category_to_delete is None:
        raise HTTPException(404, detail = f"Категория с ID {category_id} не найдена!")
    
    session.delete(category_to_delete)
    session.commit()
    return { "status": "OK" }

@app.get("/products/get_by_category")
async def get_products_by_category(category_id: int) -> List[ProductModel]:
    products = session.query(Product).filter_by(product_category = category_id).all()
    if products is None:
        return []
    
    return [ProductMapper.from_db_model(product) for product in products]

@app.patch("/products/update")
async def update_product(product_info: ProductModel):
    if product_info.product_id is None:
        raise HTTPException(400, detail = "Невозможно получить информацию о продукте без указания ID!")
    
    product_to_update = session.query(Product).filter_by(product_id = product_info.product_id).first()
    if product_to_update is None:
        raise HTTPException(400, detail = f"Продукта с ID {product_info.product_id} не существует!")
    
    product_to_update.product_name = product_info.product_name
    product_to_update.product_description = product_info.product_description
    product_to_update.product_price = product_info.product_price
    product_to_update.product_category = product_info.product_category_id
    session.add(product_to_update)
    session.commit()
    return { "status": "OK" }