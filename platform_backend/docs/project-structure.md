# Project Structure

```text
platform_backend/
├── apps/
│   ├── common/
│   ├── users/
│   ├── catalog/
│   ├── cart/
│   ├── orders/
│   ├── payments/
│   ├── reviews/
│   └── notifications/
├── config/
├── docs/
├── requirements/
├── tests/
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── manage.py
```

## Layering

- `config/`:
  Django project settings, urls, celery bootstrap
- `apps/common/`:
  shared building blocks
- `apps/users/`:
  auth, JWT, profile, roles
- `apps/catalog/`:
  product, category, discount
- `apps/cart/`:
  cart and quantity management
- `apps/orders/`:
  order placement and history
- `apps/payments/`:
  fake payment and real payment structure
- `apps/reviews/`:
  rating and comments
- `apps/notifications/`:
  notification feed and email task
