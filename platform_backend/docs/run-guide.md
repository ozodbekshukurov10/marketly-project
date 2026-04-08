# Run Guide

## 1. Requirements
- Python 3.12+
- Docker Desktop
- PostgreSQL
- Redis

## 2. Local run

```bash
cd platform_backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements/base.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 3. Celery worker

```bash
celery -A config worker -l info
```

## 4. Docker run

```bash
docker compose up --build
```

## 5. Open
- API docs: `http://127.0.0.1:8000/api/docs/`
- Admin panel: `http://127.0.0.1:8000/admin/`
