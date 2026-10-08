# Exercise 3.2 — REST API with Django REST Framework

## Overview
This submission implements Exercise 3.2: building a full CRUD REST API for the `Contact` model using Django REST Framework (DRF), complete with `ModelSerializer`, field-level validation ensuring phone numbers are strictly 10 digits, standard HTTP status codes, and routing via `DefaultRouter`.

## Architecture & Files
```
submissions/Madhumasa84/3.2/
├── manage.py
├── requirements.txt
├── README.md
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── contacts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── __init__.py
    └── management/
        └── commands/
            └── seed_contacts.py
```

## Features Implemented
1. **ModelSerializer (`contacts/serializers.py`)**:
   - Serializes `Contact` fields: `id`, `name`, `phone`, `email`, `created_at`.
   - `id` and `created_at` are configured as read-only.
   - Field-level validation: `validate_phone` ensures the phone string contains exactly 10 numeric digits, raising `serializers.ValidationError` otherwise.
2. **ModelViewSet (`contacts/views.py`)**:
   - `ContactViewSet` inherits from `rest_framework.viewsets.ModelViewSet`.
   - Supports standard REST actions: `list`, `create`, `retrieve`, `update`, `partial_update`, and `destroy`.
3. **URL Routing (`contacts/urls.py` and `project/urls.py`)**:
   - `DefaultRouter` registered under `/api/contacts/`.
4. **Appropriate HTTP Status Codes**:
   - `200 OK` on successful GET, PUT, PATCH.
   - `201 Created` on successful POST.
   - `204 No Content` on successful DELETE.
   - `400 Bad Request` on invalid input.
   - `404 Not Found` when requesting nonexistent records.

## Verification & Endpoint Test Results

### 1. GET /api/contacts/
Request:
```bash
curl -X GET http://127.0.0.1:8000/api/contacts/
```
Response: `HTTP 200 OK`
```json
[
  {
    "id": 5,
    "name": "Charlie Davis",
    "phone": "9456789013",
    "email": "charlie.davis@example.com",
    "created_at": "2026-10-08T16:00:40.456576Z"
  },
  {
    "id": 4,
    "name": "Bob Brown",
    "phone": "9345678902",
    "email": "bob.brown@example.com",
    "created_at": "2026-10-08T16:00:40.445567Z"
  }
]
```

### 2. POST /api/contacts/ (Valid Payload)
Request:
```bash
curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "phone": "9876543210", "email": "test.user@example.com"}'
```
Response: `HTTP 201 Created`
```json
{
  "id": 6,
  "name": "Test User",
  "phone": "9876543210",
  "email": "test.user@example.com",
  "created_at": "2026-10-08T16:06:57.390260Z"
}
```

### 3. POST /api/contacts/ (Invalid Phone Validation)
Request:
```bash
curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Bad Phone", "phone": "12345", "email": "bad@example.com"}'
```
Response: `HTTP 400 Bad Request`
```json
{
  "phone": [
    "Phone number must be exactly 10 digits."
  ]
}
```

### 4. GET /api/contacts/6/
Request:
```bash
curl -X GET http://127.0.0.1:8000/api/contacts/6/
```
Response: `HTTP 200 OK`
```json
{
  "id": 6,
  "name": "Test User",
  "phone": "9876543210",
  "email": "test.user@example.com",
  "created_at": "2026-10-08T16:06:57.390260Z"
}
```

### 5. PUT /api/contacts/6/
Request:
```bash
curl -X PUT http://127.0.0.1:8000/api/contacts/6/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User Updated", "phone": "9876543211", "email": "test.updated@example.com"}'
```
Response: `HTTP 200 OK`
```json
{
  "id": 6,
  "name": "Test User Updated",
  "phone": "9876543211",
  "email": "test.updated@example.com",
  "created_at": "2026-10-08T16:06:57.390260Z"
}
```

### 6. DELETE /api/contacts/6/
Request:
```bash
curl -X DELETE http://127.0.0.1:8000/api/contacts/6/
```
Response: `HTTP 204 No Content`

### 7. GET /api/contacts/6/ (Post Deletion)
Request:
```bash
curl -X GET http://127.0.0.1:8000/api/contacts/6/
```
Response: `HTTP 404 Not Found`
```json
{
  "detail": "No Contact matches the given query."
}
```
