# Marketly Backend Platform

Production-ga yaqin modular backend scaffold.

## Stack
- Python
- Django + Django Rest Framework
- PostgreSQL
- Redis
- Celery
- Docker
- JWT auth
- Swagger docs

## Arxitektura
Bu loyiha `modular monolith with clean boundaries` tarzida yozilgan.

Apps:
- `users`
- `catalog`
- `cart`
- `orders`
- `payments`
- `reviews`
- `notifications`
- `common`

## Ishga tushirish

### Docker bilan
```bash
docker compose up --build
```

### Lokal
```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements/base.txt
copy .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Swagger:
- `/api/docs/`

Admin:
- `/admin/`

## API endpointlar
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/refresh/`
- `GET/PATCH /api/auth/profile/`
- `GET/POST /api/catalog/categories/`
- `GET/POST /api/catalog/products/`
- `GET/PATCH/DELETE /api/catalog/products/{id}/`
- `GET/POST /api/catalog/discounts/`
- `GET /api/cart/`
- `POST /api/cart/items/`
- `DELETE /api/cart/items/`
- `GET/POST /api/orders/`
- `GET/PATCH/DELETE /api/orders/{id}/`
- `POST /api/payments/`
- `GET /api/payments/providers/`
- `GET/POST /api/reviews/`
- `GET/PATCH/DELETE /api/reviews/{id}/`
- `GET /api/notifications/`
