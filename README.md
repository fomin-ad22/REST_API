# REST_API
REST API project on FAST API with product and category-related methods (SQLModel DB connection, API pytest control).

Cервис предоставляет методы для работы с продуктами и категориями интернет-магазина. 
Также реализована возможность подключения к БД и хранению данных в ней (В текущем проекте SQLlite).

Основные классы:

• test_product=Product({'name':"Product C", 'description':"Description for Product QWE", 'price':15.00, 'category_id':2, 'image_url':"https://example.com/image2.jpg", 'stock':20, 'created_at':"2023-03-16T12:00:00Z", '    updated_at':"2023-03-16T12:00:00Z"})

• test_category=Category({'name':"Lemon"})

Основные функции:

Продукты:

• Создание продукта: Добавляйте новые продукты в ваш каталог create_product(test_Product).
• Обновление продукта: Заменяйте существующий продукт по его id update_product(product_id, test_product).
• Удаление продукта: Удаляйте продукт из каталога по его id del_product(product_id).
• Поиск продукта: Находите нужный продукт по его id get_product(product_id).
• Вывод продуктов: Выводите актуальный каталог продуктов get_products().
• Фильтрация продуктов: Фильтруйте продукты по их id, названию, минимальной и максимальной цене filter_products(product_id,"A",15,20).

Категории:

• Создание категории: Создавайте новые категории продуктов create_category(test_category).
• Удаление категории: Удаляйте существующие категории продуктов по их id del_category(category_id). 
• Поиск категории: Находите нужную категорию по ее id get_category(category_id).
• Вывод категорий: Выводите актуальные категории get_categories().

Как использовать сервис:

Для работы с сервисом вам необходимо из рабочей директории запустить API через терминал командой "uvicorn main:app".  
Взаимодействие с сервисом осуществляется через файл client.py путем запуска нужной функции.


С вопросами и предложениями @fomin_ad22 tg
