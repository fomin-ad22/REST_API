from typing import List
from fastapi import FastAPI, HTTPException, status,Depends
from models import Product,Category
from sqlalchemy import create_engine,select
from sqlmodel import SQLModel,Session,create_engine,select

engine = create_engine("sqlite:///./database.db",connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/products", response_model=List[Product])                                                               
async def get_products(session: Session = Depends(get_session)):
    print("Вывод всех Продуктов:")
    products_from_bd = session.exec(select(Product))
    for products in session.exec(select(Product)):
        print(products )
    print("Вывод Продуктов завершен")
    return products_from_bd

@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int,session: Session = Depends(get_session)):
    print(f"Вывод Продукта с id = {product_id}:")
    found_product = next(session.exec(select(Product).where(Product.id==product_id)),None)
    print(found_product)
    if(found_product is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    print("Вывод Продукта завершен")
    return found_product

@app.post("/products/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(newProduct: Product,session: Session = Depends(get_session)):
    print("Создание нового Продукта:")
    session.add(newProduct)
    session.commit()
    session.refresh(newProduct)
    print(newProduct)
    print("Создание Продукта завершено")
    return newProduct

@app.put("/products/{product_id}", response_model=Product)                                                                 
async def update_product(product_id: int, product: Product,session: Session = Depends(get_session)):
    print(f"Изменение продукта с id = {product_id}:")
    found_product = session.get(Product,product_id)
    if( found_product is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    found_product.name=product.name
    found_product.description=product.description
    found_product.price=product.price
    found_product.category=product.category
    found_product.image_url=product.image_url
    found_product.stock=product.stock
    found_product.created_at=product.created_at
    found_product.updated_at=product.updated_at
    session.commit()
    session.refresh(found_product)

    print(f"Обновлена информация. Новый продукт: \n{found_product}")
    return found_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)                                         
async def delete_product(product_id: int,session: Session = Depends(get_session)):
    print(f"Удаление Продукта с id = {product_id}")
    delete_product = session.get(Product,product_id)
    if(delete_product is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    session.delete(delete_product)
    session.commit()
    print(f"Удален продукт: {delete_product}")

@app.get("/categories", response_model=List[Category])                          
async def get_categories(session: Session = Depends(get_session)):
    print("Вывод Категорий:")
    found_catefories=session.exec(select(Category))
    for categories in session.exec(select(Category)):
        print(categories)
    print("Вывод Категорий Завершен")
    return found_catefories

@app.get("/categories/{category_id}", response_model=Category)
async def get_category(category_id: int,session: Session = Depends(get_session)):
    print(f"Поиск категории с id = {category_id}")
    found_category = next(session.exec(select(Category).where(Category.id==category_id)),None)
    if(found_category is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    print(f"Категория найдена: \n{found_category}")
    return found_category

@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)                        
async def create_category(new_category: Category,session: Session = Depends(get_session)):
    print("Создание Категории:")
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    print(new_category)
    print("Категория создана")
    return new_category

@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)                               
async def delete_category(category_id: int,session: Session = Depends(get_session)):
    print("Удаление Категории")
    delete_category=session.get(Category,category_id)

    if(delete_category is None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    session.delete(delete_category)
    session.commit()
    print(f"Удалена категория: \n{delete_category}")


def check_conditions(item:Product,categoryId,keywords:str,price_min:float,price_max:float):
    if categoryId!=-1 and item.category_id!=categoryId:
        return 
    elif keywords!="-1" and keywords.lower() not in item.name.lower():
        return
    elif price_min!=-1 and price_min>item.price:
        return
    elif price_max!=-1 and price_max<item.price:
        return 
    else:
        return True
        
@app.get("/products/filter/{categoryId}/{keywords}/{price_min}/{price_max}", response_model=List[Product])
async def filter_products(categoryId: int, keywords: str, price_min: float, price_max:float,session: Session = Depends(get_session)):
    print(f"Сортировка продуктов по параметрам categoryID = {categoryId}, keywords = {keywords}, price_min = {price_min}, price_max = {price_max}:")
    
    products_bd=session.exec(select(Product)).all()
    filtred_products=[product for product in products_bd if check_conditions(product,categoryId,keywords,price_min,price_max)]

    print(f"{filtred_products} \nВывод продуктов завершен ")
    return filtred_products

# #      rm database.db    (from shell)
# #      cd C:\Users\artem\.vscode\server\api
# #      uvicorn main:app
