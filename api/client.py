import requests

BASE_URL = "http://127.0.0.1:8000"

def create_product(product_data):                                           
  response = requests.post(f"{BASE_URL}/products/", json=product_data)
  if (response.status_code == 201):
    return response
  else:
    raise Exception(f"Ошибка создания продукта: {response.text}")
  
def get_products():
  response = requests.get(f"{BASE_URL}/products")
  if (response.status_code == 200):
    return response
  else:
    raise Exception(f"Ошибка получения продуктов: {response.text}")

def get_product(product_id):
  response = requests.get(f"{BASE_URL}/products/{product_id}")
  if (response.status_code == 200):
    return response
  else:
    raise Exception(f"Ошибка получения продукта: {response.text}")

def update_product(product_id,product_data):
  response = requests.put(f"{BASE_URL}/products/{product_id}",json=product_data)
  return response

def del_product(product_id):
  response = requests.delete(f"{BASE_URL}/products/{product_id}")

def get_categories():                                                       
  response = requests.get(f"{BASE_URL}/categories") 
  if (response.status_code == 200):
    return response
  else:
    raise Exception(f"Ошибка получения категорий: {response.text}")   

def get_category(category_id):
  response = requests.get(f"{BASE_URL}/categories/{category_id}")
  if (response.status_code == 200):
    return response
  else:
    raise Exception(f"Ошибка получения категорий: {response.text}")   

def create_category(category_data):                                                 
  response = requests.post(f"{BASE_URL}/categories", json=category_data)
  if (response.status_code == 201):
    return response
  else:
    raise Exception(f"Ошибка создания категории: {response.text}")
  
def del_category(category_id):
  response = requests.delete(f"{BASE_URL}/categories/{category_id}")

def filter_products(categoryId, keywords, price_min, price_max):
  response = requests.get(f"{BASE_URL}/products/filter/{categoryId}/{keywords}/{price_min}/{price_max}")
  if (response.status_code == 200):
    return response
  else:
    raise Exception(f"Ошибка получения продуктов: {response.text}")
  

#Main typs:

# testCategory={'name':"Lemon"}
testProd={'name':"Product B", 'description':"Description for Product QWE", 'price':15.00, 'category_id':2, 'image_url':"https://example.com/image2.jpg", 'stock':20, 'created_at':"2023-03-16T12:00:00Z", 'updated_at':"2023-03-16T12:00:00Z"}

# Main commands: 

# create_product(testProd)
# get_products()
# get_product(2)
# update_product(1,testProd)
# del_product(1)

# get_categories()
# create_category(testCategory)
#get_category(3)
# del_category(3)

# filter_products(2,"B",10,20) # передавать все 4 значения (-1 в случае отсутствия )