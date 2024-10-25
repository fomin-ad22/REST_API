from ..api import client
from ..api.models import Product,Category
import pytest
from sqlalchemy import create_engine,select
from sqlmodel import Session,create_engine,select
import random

@pytest.fixture
def get_engine():
    return create_engine("sqlite:///../api/database.db",connect_args={"check_same_thread": False})

@pytest.fixture                                
def get_session(get_engine):
    with Session(get_engine) as session:
        yield session


@pytest.fixture
def get_client():
    return client

def test_create_product(get_client):
    product_data = {
      "name": "Test Product",
      "description": "Test description",
      "price": 10.0,
      "category_id": 1, 
      "image_url": "https://example.com/image.jpg",
      "stock": 10,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    response = get_client.create_product(product_data)
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]
    assert response.json()["price"] == product_data["price"]

def test_get_products(get_client,get_session):

    response = get_client.get_products()
    assert response.status_code == 200
    products_in_bd=get_session.exec(select(Product)).all()
    

    assert len(response.json()) == len(products_in_bd)

def test_get_product_by_id(get_client, get_session):
    special_id = random.randint(1000,2000)
    product_data = {
      "id":special_id,
      "name": "Special_Product",
      "description": "Test description",
      "price": 10.0,
      "category_id": 1, 
      "image_url": "https://example.com/image.jpg",
      "stock": 10,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    get_client.create_product(product_data) 
    response = get_client.get_product(special_id)
    assert response.status_code == 200 
    
    bd_products=get_session.exec(select(Product).where(Product.id==special_id)).all()  
    assert response.json()["id"]==bd_products[0].id

def test_update_product(get_client,get_session):

    special_id = random.randint(1000,2000)
    product_data = {
      "id":special_id,
      "name": "Special_Product",
      "description": "Test description",
      "price": 10.0,
      "category_id": 1, 
      "image_url": "https://example.com/image.jpg",
      "stock": 10,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    get_client.create_product(product_data) 
    update_description = "Update_description"
    update_product_data = {
      "id":special_id,
      "name": "Update_Special_Product",
      "description": update_description,
      "price": 20.0,
      "category_id": 1, 
      "image_url": "https://example.com/image.jpg",
      "stock": 10,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    response = get_client.update_product(special_id,update_product_data)
    assert response.status_code==200
    bd_product = get_session.get(Product,special_id)
    assert response.json()["description"]==bd_product.description and bd_product.description == update_description 


def test_del_product(get_client,get_session):
    special_id = random.randint(1000,2000)
    product_data = {
      "id":special_id,
      "name": "Special_Product",
      "description": "Test description",
      "price": 10.0,
      "category_id": 1, 
      "image_url": "https://example.com/image.jpg",
      "stock": 10,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
    get_client.create_product(product_data)
    response = get_client.get_product(special_id)
    assert response.status_code == 200

    response=get_client.del_product(special_id)

    bd_products=get_session.exec(select(Product).where(Product.id==special_id)).all() 
    assert len(bd_products)==0

def test_get_categories(get_client,get_session):
    testCategory={'name':"TestCategory"}
    response = get_client.create_category(testCategory)
    assert response.status_code == 201

    response = get_client.get_categories()
    assert response.status_code==200
    bd_categories = get_session.exec(select(Category)).all()

    assert len(response.json())==len(bd_categories)

def test_get_category(get_client,get_session):
    special_id = random.randint(1000,2000)
    testCategory={'id':special_id,'name':"TestCategory"}
    response = get_client.create_category(testCategory)
    assert response.status_code==201

    response = get_client.get_category(special_id)
    assert response.status_code==200

    bd_category = get_session.get(Category,special_id)
    assert response.json()["id"]==bd_category.id and bd_category.id == special_id

def test_create_category(get_client,get_session):
    name_category = "SpecialCategory"
    testCategory={'name':name_category}
    response = get_client.create_category(testCategory)
    assert response.status_code == 201
    assert response.json()["name"]==name_category

    bd_category = get_session.exec(select(Category).where(Category.name ==name_category )).all()
    assert len(bd_category)!=0 and bd_category[0].name == name_category

def test_del_category(get_client,get_session):
    special_id = random.randint(1000,2000)
    testCategory={'id':special_id,'name':"SpecialCategory"}
    response = get_client.create_category(testCategory)
    assert response.status_code == 201

    response = get_client.del_category(special_id)

    bd_categories = get_session.exec(select(Category).where(Category.id==special_id)).all()
    assert len(bd_categories)==0

def test_filter_products(get_client):
    
    response=get_client.filter_products(1,-1,-1,-1)
    assert response.status_code ==200
    response=get_client.filter_products(-1,"Test",-1,-1)
    assert response.status_code ==200
    response=get_client.filter_products(-1,-1,10,30)
    assert response.status_code ==200 
    response=get_client.filter_products(2,-1,10,20)
    assert response.status_code ==200