**QR-sys FastAPI backend app**


# По етапний гайд як ініціалізувати додаток вручу

1. Встановлення всіх залежностей 

```bash
user@~: pip install -r requirements.txt
```
2. Також потрібно запустити PostgreSQL базу данних через докер або pgAdmin
   та вказати посилання в файлі *app/settings.py*. Заповнити потрібно обидві константи
    як DATABASE (асинхронне підключення) та DATABASE_SYNC (синхроне).

3. Ініціалізація бази данних та створення всіх таблиць

```bash
user@~: alembic revision --autogenerate
user@~: alembic upgrade head
```

4. Так само потрібно запустити redis, він відповідає за збережння куків користувача.
   Налаштування порту, хосту та бази данних також знаходяться в *app/settings.py*.


5. Запуск celery для фонових задач (напр. відправка email)

```bash
user@~: celery --app=app.framework.celery.object:celery worker -l INFO
```

6. Запуск flower для візуального перегляду фонових задач
   
```bash
user@~: celery --app=app.framework.celery.object:celery flower
```

7. Генерація секретного ключа для JWT токенів

```bash
user@~: python3 -m app.SECRET_KEY.generate --set-secret
```


8. DEBUG = False тільки якщо для запуску продакшн середовища через
   docker-compose.yml, для середовища розробки DEBUG = True.
 
9. Запуск додатку

```bash
user@~: uvicorn app.API.api:app --host:<host> --port:<port>
```

* Або можете запустити додаток за допомогою *Dockerfile*


# Файлова система проекту qr-sys

- app
    - API
        - api <-- Головна папка з функціями нашого API
            ...
        - QR <-- Обьект для взаємодії з QR, генерація, видалення, збереження, отримання
            ...
        - ResponseModels <-- pydantic моделі для валідації исходящих відповідей від серверу
            ...
        - ValidationModels <-- pydantic моделі для валідації входящих запитів від клієнту
            ...
        - tests <-- тести для додатку

    - database 
        - db
            - Meta 
                - data <-- Мета дата для таблиць бд
                - engine_async <-- Ініціалізація асинхроного підключення до бд
                - engine_sync <-- Ініціалізація синхронго підключення до бд 

            - models
                - _async <-- Асинхрона модель для взаємодії з бд
                - sync <-- Синхрона модель для взаємодії з бд
            
            - TablesParse <-- Філтрує обьєкти таблиць  
                ... 

        - tables.py <-- Тут описуються всі таблиці додатку для їх створення треба використовувати alembic

    - framework
        - JWT
            - MetaData
                - jwt_metadata.py <-- Обьєкт через який відбувається взаємодія з JWT хешованимим токенами (отримання, видалення)
            - token 
                - auth.py <-- Обьєкт який створює та перевіряє дійсність JWT токенів, також через нього
                                відбувається взаємодія з каталогом MetaData
            - validation <-- Перевіряє входящі токени в запиті та валідує їх також повертає токен якщо він дійсний 
                ...
            - trash_methods
                - trash.py <-- Обьєкт для методів які незнаєш куди пихнути
        - celery <-- виконує фонові задачі
           ...
        - email <-- взаєиодія з SMTP клієнтом 
           ...
        - recovery <-- обьєкт для створення праолю відновлення для користувача
           ...
        - redis <-- Зберігає в кеші JWT токени користувачів
           ...
    - settings.py <-- Налаштування для проекту 


# Версія 0.0.1-ps

> Використовує PostgreSQL базу данних

# Вкрсія latest
> + Redis
> + Celery
> + Flower
