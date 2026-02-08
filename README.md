# Backend для автоматизации закупок

REST API на Django + DRF для розничной сети: клиенты делают заказы, поставщики получают уведомления.

## Быстрый запуск

```bash
# 1. Клонировать (если нужно)
git clone <ваш-репозиторий>
cd procurement-automation

# 2. Виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/macOS/WSL
# venv\Scripts\activate   # Windows

# 3. Зависимости
pip install -r requirements.txt

# 4. Миграции
python manage.py migrate

# 5. (Опционально) Суперпользователь
python manage.py createsuperuser

# 6. Запуск
python manage.py runserver
```

## API Endpoints
### Аутентификация
```
POST /api/auth/register/ — регистрация
Тело: {"username": "...", "email": "...", "password": "...", "password2": "..."}

POST /api/auth/login/ — вход (возвращает токен)
Тело: {"username": "...", "password": "..."}
```

### Товары
```
GET /api/products/ — каталог товаров
GET /api/products/{id}/` — детали товара
```
# Заказы
```
POST /api/orders/ — создать заказ
Тело: {
    "delivery_address": "Адрес",
    "items": [{"product_id": 1, "quantity": 2}]
    }

GET /api/orders/my/ — мои заказы
GET /api/orders/<id>/ — детали заказа
```

Все эндпоинты требуют заголовок:
```
Authorization: Token ваш_токен
```

### Импорт товаров
Товары можно загружать из YAML-файлов:
```bash
python manage.py import_products data/sample.yaml
```

Формат файла:
```yaml
supplier:
  company_name: "Название компании"
  email: "postavshik@example.com"
  accepts_orders: true

products:
  - name: "Товар 1"
    price: 100.00
    description: "Описание"
    attributes:
      - name: "Цвет"
        value: "Красный"
```

## Примечание
Email-уведомления выводятся в консоль (настройка EMAIL_BACKEND = 'console').

```bash
# 1. Регистрация клиента
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"client","email":"client@example.com","password":"pass123","password2":"pass2123"}'

#  2. Получите список товаров
curl -H "Authorization: Token ВАШ_ТОКЕН" http://127.0.0.1:8000/api/products/

# 3. Создайте заказ
curl -X POST http://127.0.0.1:8000/api/orders/ \
  -H "Authorization: Token ВАШ_ТОКЕН" \
  -H "Content-Type: application/json" \
  -d '{"delivery_address":"СПБ, Кораблестроителей 1","items":[{"product_id":1,"quantity":1}]}'

# 4. Посмотрите список заказов
curl -H "Authorization: Token ВАШ_ТОКЕН" http://127.0.0.1:8000/api/orders/my/

# 5. Посмотрите детали заказа
curl -H "Authorization: Token ВАШ_ТОКЕН" http://127.0.0.1:8000/api/orders/ВАШ_ID/