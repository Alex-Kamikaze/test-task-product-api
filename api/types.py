import abc

from pydantic import BaseModel
from api.models import Category, Product

class ModelMapper(abc.ABC):
    """ Вспомогательный класс для создания мапперов между моделями БД и моделями API """
    @abc.abstractmethod
    def from_db_model(): pass

    @abc.abstractmethod
    def into_db_model(): pass


class CategoryModel(BaseModel):
    """ Модель категории в API """
    category_id: int
    category_name: str

class ProductModel(BaseModel):
    """ Модель продукта в API """
    product_id: int | None = None # Нужно для ситуаций, когда id будет задан БД, а не пользователем. В случае добавления нового товара, id в запросе указывать не требуется
    product_name: str
    product_description: str
    product_price: int
    product_category_id: int

class UserRegistrationModel(BaseModel):
    """ Модель с данными пользователя в API """
    user_login: str
    user_password: str

class CategoryMapper(ModelMapper):
    """ Маппер между категориями в БД и API """
    def from_db_model(category_db: Category) -> CategoryModel:
        return CategoryModel(category_id = category_db.category_id, category_name = category_db.category_name)
    
    def into_db_model(category_model: CategoryModel) -> Category:
        return Category(category_id = category_model.category_id, category_name = category_model.category_name)
    
class ProductMapper(ModelMapper):
    """ Маппер между продуктами в БД и API """
    def from_db_model(product: Product) -> ProductModel:
        return ProductModel(product_id = product.product_id, product_name = product.product_name, product_description = product.product_description, product_price = product.product_price, product_category_id = product.product_category)
    
    def into_db_model(product_model: ProductModel) -> Product:
        return Product(product_id = product_model.product_id, product_name = product_model.product_name, product_description = product_model.product_description, product_price = product_model.product_price,product_category = product_model.product_category_id)

    
