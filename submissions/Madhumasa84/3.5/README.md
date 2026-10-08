# Exercise 3.5 — Authentication & Permissions

## Overview
This submission implements Exercise 3.5: adding Token Authentication to the Contact REST API, enforcing that write operations (`POST` and `DELETE`) require authentication while read operations (`GET`) remain publicly accessible without credentials, and providing a dedicated `/api/auth/login/` endpoint that generates and returns an authentication token for valid user credentials.

## Architecture & Files
```
submissions/Madhumasa84/3.5/
├── manage.py
├── requirements.txt
├── README.md
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── celery.py
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
    ├── tasks.py
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
1. **Token Authentication Configuration (`project/settings.py`)**:
   - Added `rest_framework.authtoken` to `INSTALLED_APPS`.
   - Configured `DEFAULT_AUTHENTICATION_CLASSES` with `TokenAuthentication` and `SessionAuthentication`.
2. **Action-Based Permission Control (`contacts/views.py`)**:
   - Overrode `get_permissions()` in `ContactViewSet`:
     - Safe read actions (`list`, `retrieve`, or HTTP `GET`) use `AllowAny` (publicly accessible).
     - Write actions (`create`, `destroy`, `update`, etc.) require `IsAuthenticated`.
3. **Authentication Endpoint (`/api/auth/login/`)**:
   - Implemented `LoginView` at `/api/auth/login/`.
   - Accepts JSON payload containing `username` and `password`.
   - Authenticates credentials against Django's authentication system.
   - Generates or retrieves token via `Token.objects.get_or_create(user=user)`.
   - Returns `{ "token": "<token_key>", "user_id": <id>, "username": "<username>" }`.
   - Returns `HTTP 400 Bad Request` if fields are missing.
   - Returns `HTTP 401 Unauthorized` for invalid credentials.
4. **Automated Unit Tests (`contacts/tests.py`)**:
   - 9 test cases covering public GET access, protected POST/DELETE rejection without token, login credential validation, successful token retrieval, and authenticated POST/DELETE execution.

## Verification & Endpoint Test Results

### 1. GET /api/contacts/ (Unauthenticated - Allowed)
Request:
```bash
curl -X GET http://127.0.0.1:8000/api/contacts/
```
Response: `HTTP 200 OK`
```json
{
  "count": 11,
  "next": "http://127.0.0.1:8000/api/contacts/?page=2",
  "previous": null,
  "results": [ ... ]
}
```

### 2. POST /api/contacts/ (Unauthenticated - Rejected)
Request:
```bash
curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Anon", "phone": "9876543210", "email": "anon@example.com"}'
```
Response: `HTTP 401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 3. DELETE /api/contacts/1/ (Unauthenticated - Rejected)
Request:
```bash
curl -X DELETE http://127.0.0.1:8000/api/contacts/1/
```
Response: `HTTP 401 Unauthorized`
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 4. POST /api/auth/login/ (Obtain Token)
Request:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```
Response: `HTTP 200 OK`
```json
{
  "token": "e352ad9a9a36f143294493abc0427662219f19d6",
  "user_id": 2,
  "username": "testuser"
}
```

### 5. POST /api/contacts/ (Authenticated with Token - Allowed)
Request:
```bash
curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token e352ad9a9a36f143294493abc0427662219f19d6" \
  -d '{"name": "Auth User", "phone": "9876543210", "email": "auth@example.com"}'
```
Response: `HTTP 201 Created`
```json
{
  "id": 13,
  "name": "Auth User",
  "phone": "9876543210",
  "email": "auth@example.com",
  "created_at": "2026-10-08T17:50:12.048117Z"
}
```

### 6. DELETE /api/contacts/13/ (Authenticated with Token - Allowed)
Request:
```bash
curl -X DELETE http://127.0.0.1:8000/api/contacts/13/ \
  -H "Authorization: Token e352ad9a9a36f143294493abc0427662219f19d6"
```
Response: `HTTP 204 No Content`

### 7. Automated Test Suite Run
```bash
python manage.py test contacts
```
Output:
```text
Ran 9 tests in 3.168s
OK
```
