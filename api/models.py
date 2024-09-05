from sqlalchemy import Column, Float, String, create_engine, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
db = create_engine('sqlite:///products.db')

Base.metadata.bind = db

class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)
    products = relationship("Product", backref="categories")

    def __str__(self):
        return self.category_name
    
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_login = Column(String, nullable=False, unique = True)
    user_password = Column(String, nullable=False)

    def __str__(self):
        return f"{self.user_id}:{self.user_login}"


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable = False, unique = True)
    product_description = Column(String, nullable = True)
    product_price = Column(Integer, default = 0)
    product_category = Column(Integer, ForeignKey("categories.category_id", ondelete="CASCADE"))
    category = relationship("Category", back_populates = "products")

session_meta = sessionmaker(autoflush=False, bind=db)
session = session_meta()