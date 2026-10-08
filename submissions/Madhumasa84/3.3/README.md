# Exercise 3.3 — Filtering, Search & Pagination

## Overview
This submission implements Exercise 3.3: extending the Contact REST API with query parameter filtering, full-text search, and page-based pagination using `django-filter` and Django REST Framework's built-in filter and pagination classes.

## Architecture & Files
```
submissions/Madhumasa84/3.3/
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
    ├── pagination.py
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
1. **Query Parameter Filtering (`DjangoFilterBackend`)**:
   - Integrated `django_filters.rest_framework.DjangoFilterBackend`.
   - Enabled filtering on `email`, `phone`, and `name` via query parameters (e.g., `?email=john.doe@example.com`).
2. **Search Filter (`SearchFilter`)**:
   - Integrated `rest_framework.filters.SearchFilter`.
   - Enabled searching across `name`, `email`, and `phone` via `?search=John`.
3. **Pagination (`PageNumberPagination`)**:
   - Configured `ContactPagination` subclassing `PageNumberPagination` with `page_size = 5`.
   - Supports page traversal via `?page=2`.
   - Returns paginated envelopes containing `count`, `next`, `previous`, and `results`.
4. **Ordering (`OrderingFilter`)**:
   - Enabled ordering by `name` and `created_at`.

## Verification & Endpoint Test Results

### 1. Filtering by Email: GET /api/contacts/?email=john.doe@example.com
Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/contacts/?email=john.doe@example.com"
```
Response: `HTTP 200 OK`
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "John Doe",
      "phone": "9876543210",
      "email": "john.doe@example.com",
      "created_at": "2026-10-08T16:00:40.412937Z"
    }
  ]
}
```

### 2. Search by Name: GET /api/contacts/?search=John
Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/contacts/?search=John"
```
Response: `HTTP 200 OK`
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "name": "Alice Johnson",
      "phone": "9234567891",
      "email": "alice.johnson@example.com",
      "created_at": "2026-10-08T16:00:40.433639Z"
    },
    {
      "id": 1,
      "name": "John Doe",
      "phone": "9876543210",
      "email": "john.doe@example.com",
      "created_at": "2026-10-08T16:00:40.412937Z"
    }
  ]
}
```

### 3. Pagination Page 1: GET /api/contacts/?page=1
Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/contacts/?page=1"
```
Response: `HTTP 200 OK`
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/contacts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 11,
      "name": "User 10",
      "phone": "9876543210",
      "email": "user10@example.com",
      "created_at": "2026-10-08T16:13:31.837560Z"
    },
    {
      "id": 10,
      "name": "User 9",
      "phone": "9876543209",
      "email": "user9@example.com",
      "created_at": "2026-10-08T16:13:31.828675Z"
    },
    {
      "id": 9,
      "name": "User 8",
      "phone": "9876543208",
      "email": "user8@example.com",
      "created_at": "2026-10-08T16:13:31.818888Z"
    },
    {
      "id": 8,
      "name": "User 7",
      "phone": "9876543207",
      "email": "user7@example.com",
      "created_at": "2026-10-08T16:13:31.808560Z"
    },
    {
      "id": 7,
      "name": "User 6",
      "phone": "9876543206",
      "email": "user6@example.com",
      "created_at": "2026-10-08T16:13:31.796437Z"
    }
  ]
}
```

### 4. Pagination Page 2: GET /api/contacts/?page=2
Request:
```bash
curl -X GET "http://127.0.0.1:8000/api/contacts/?page=2"
```
Response: `HTTP 200 OK`
```json
{
  "count": 10,
  "next": null,
  "previous": "http://127.0.0.1:8000/api/contacts/",
  "results": [
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
    },
    {
      "id": 3,
      "name": "Alice Johnson",
      "phone": "9234567891",
      "email": "alice.johnson@example.com",
      "created_at": "2026-10-08T16:00:40.433639Z"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "phone": "9123456780",
      "email": "jane.smith@example.com",
      "created_at": "2026-10-08T16:00:40.422917Z"
    },
    {
      "id": 1,
      "name": "John Doe",
      "phone": "9876543210",
      "email": "john.doe@example.com",
      "created_at": "2026-10-08T16:00:40.412937Z"
    }
  ]
}
```
