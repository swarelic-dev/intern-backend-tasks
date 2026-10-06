# 🐍 Backend Exercises 3.1 – 3.5: Django REST API with Contacts

## Overview
Full implementation of all 5 backend exercises for the `intern-backend-tasks` repo using Django 6.1, Django REST Framework 3.18, Celery 5.6, and Redis.

---

## Exercise 3.1 — Django Setup & Contact Model

- Created Django project using `django-admin startproject`
- Created `contacts` app with `Contact` model:
  - `name` (CharField)
  - `phone` (CharField, 10 digits)
  - `email` (EmailField)
  - `created_at` (DateTimeField, auto_now_add)
- Registered `Contact` in Django Admin with `list_display`
- Ran migrations: all applied successfully
- Management command `seed_contacts` seeds 5 dummy contacts using `bulk_create`

---

## Exercise 3.2 — REST API with Django REST Framework

Full CRUD API using `ModelViewSet` and `DefaultRouter`:

| Method | URL | Description |
|--------|-----|-------------|
| GET    | `/api/contacts/` | List all contacts |
| POST   | `/api/contacts/` | Create a contact |
| GET    | `/api/contacts/<id>/` | Retrieve single contact |
| PUT    | `/api/contacts/<id>/` | Update a contact |
| DELETE | `/api/contacts/<id>/` | Delete a contact |

- `ContactSerializer` using `ModelSerializer`
- Phone validation: exactly 10 digits (validated in `validate_phone`)
- Proper HTTP status codes (200, 201, 204, 400, 401, 404)

---

## Exercise 3.3 — Filtering, Search & Pagination

- **Filter by email**: `GET /api/contacts/?email=alice@example.com`
- **Search by name**: `GET /api/contacts/?search=John`
- **Pagination**: 5 results per page, `GET /api/contacts/?page=2`
- Uses `DjangoFilterBackend`, `SearchFilter`, `PageNumberPagination` (PAGE_SIZE=5)

---

## Exercise 3.4 — Background Task with Celery

- Celery configured with Redis broker (`redis://localhost:6379/0`)
- `send_welcome_sms` task dispatched via `.delay()` on POST `/api/contacts/`
- Task logs "Sending SMS to `<phone>`: Welcome to SCAI!" using Python logging

**Worker output:**
```
[2026-10-06 14:20:04,064: INFO/MainProcess] Task contacts.tasks.send_welcome_sms[003f9493-d0c9-489c-ad39-0fa4fe2a95e8] received
[2026-10-06 14:20:04,066: INFO/MainProcess] Sending SMS to 1231231234: Welcome to SCAI!
[2026-10-06 14:20:04,069: INFO/MainProcess] Task contacts.tasks.send_welcome_sms[003f9493-d0c9-489c-ad39-0fa4fe2a95e8] succeeded in 0.004432292014826089s: 'SMS sent to 1231231234'
```

---

## Exercise 3.5 — Authentication & Permissions

- **Token Authentication** via DRF's `TokenAuthentication`
- `POST /api/contacts/` — requires `Authorization: Token <token>`
- `DELETE /api/contacts/<id>/` — requires `Authorization: Token <token>`
- `GET /api/contacts/` — publicly accessible (no auth required)
- `POST /api/auth/login/` — returns token for valid credentials using DRF's `obtain_auth_token`

---

## API Test Results

See [PR_DESCRIPTION.md](PR_DESCRIPTION.md) for full curl/HTTP request-response results.

### Quick Summary

| Test | Status |
|------|--------|
| List all contacts (GET) | ✅ 200 |
| Filter by email | ✅ 200 |
| Search by name | ✅ 200 |
| Pagination | ✅ 404 on empty page |
| Create contact (POST + Auth) | ✅ 201 |
| Retrieve single contact (GET) | ✅ 200 |
| Update contact (PUT + Auth) | ✅ 200 |
| Delete contact (DELETE + Auth) | ✅ 204 |
| Invalid phone validation | ✅ 400 |

---

## Running Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Seed contacts
python manage.py seed_contacts

# Create superuser
python manage.py createsuperuser

# Start dev server
python manage.py runserver

# Start Celery worker (requires Redis)
celery -A project worker --pool=solo -l info
```
