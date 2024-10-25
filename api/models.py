from sqlmodel import SQLModel, Field,Relationship,create_engine
from typing import Optional,ClassVar,List
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import Integer


class Category(SQLModel,table = True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name:Optional[str]=Field(default=None,nullable=True)
    products:List["Product"]=Relationship(back_populates="category")


class Product(SQLModel,table = True):
    id:Optional[int]=Field(default=None,primary_key=True)
    name: Optional[str]=Field(default=None,nullable=True)
    description: Optional[str]=Field(default=None,nullable=True)
    price: Optional[float]=Field(default=None,nullable=True)
    category_id: Optional[int]=Field(default=None,foreign_key="category.id")
    image_url: Optional[str]=Field(default=None,nullable=True)
    stock: Optional[int]=Field(default=None,nullable=True)
    created_at: Optional[str]=Field(default=None,nullable=True)
    updated_at: Optional[str]=Field(default=None,nullable=True)
    category:Optional[Category]=Relationship(back_populates="products")

#test models