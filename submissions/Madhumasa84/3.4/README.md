# Exercise 3.4 — Background Task with Celery

## Overview
This submission implements Exercise 3.4: configuring Celery with Redis as the message broker, creating the `send_welcome_sms` asynchronous task, dispatching the task on `POST /api/contacts/` using the `.delay()` pattern, and verifying task execution in the worker output logs.

This mirrors the `dispatch_event_async()` pattern used in the SCAI rules engine.

## Architecture & Files
```
submissions/Madhumasa84/3.4/
├── manage.py
├── requirements.txt
├── README.md
├── worker_output.log
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
1. **Redis Broker in Docker**:
   - Spun up Redis broker via Docker:
     ```bash
     docker run -d --name scai-redis -p 6379:6379 redis:alpine
     ```
2. **Celery Configuration (`project/celery.py` & `project/__init__.py`)**:
   - Created Celery application instance configured to read settings with prefix `CELERY_`.
   - Enabled `autodiscover_tasks()`.
   - Exported `celery_app` in `project/__init__.py`.
3. **Django Settings (`project/settings.py`)**:
   - `CELERY_BROKER_URL = 'redis://localhost:6379/0'`
   - `CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'`
   - `CELERY_ACCEPT_CONTENT = ['json']`
   - `CELERY_TASK_SERIALIZER = 'json'`
   - `CELERY_RESULT_SERIALIZER = 'json'`
4. **Celery Task (`contacts/tasks.py`)**:
   - Defined `@shared_task def send_welcome_sms(phone)`.
   - Uses standard Python `logging` to log: `"Sending SMS to <phone>: Welcome to SCAI!"`.
5. **Asynchronous Dispatch (`contacts/views.py`)**:
   - Overrode `perform_create` on `ContactViewSet`.
   - Dispatches `send_welcome_sms.delay(contact.phone)` upon contact creation.

## Verification & Worker Output

### 1. Trigger POST /api/contacts/
Request:
```bash
curl -X POST http://127.0.0.1:8000/api/contacts/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Bruce Banner", "phone": "9876543210", "email": "bruce.banner@example.com"}'
```
Response: `HTTP 201 Created`
```json
{
  "id": 12,
  "name": "Bruce Banner",
  "phone": "9876543210",
  "email": "bruce.banner@example.com",
  "created_at": "2026-10-08T17:45:33.260885Z"
}
```

### 2. Celery Worker Log Output
```text
[2026-10-08 17:45:33,371: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-10-08 17:45:33,393: INFO/MainProcess] mingle: searching for neighbors
[2026-10-08 17:45:34,431: INFO/MainProcess] mingle: all alone
[2026-10-08 17:45:34,499: INFO/MainProcess] celery@DESKTOP-HDA6H4T ready.
[2026-10-08 17:45:34,514: INFO/MainProcess] Task contacts.tasks.send_welcome_sms[c1a6ad2d-789b-49d5-86df-b15c2f55106a] received
[2026-10-08 17:45:34,519: INFO/ForkPoolWorker-8] Sending SMS to 9876543210: Welcome to SCAI!
[2026-10-08 17:45:34,579: INFO/ForkPoolWorker-8] Task contacts.tasks.send_welcome_sms[c1a6ad2d-789b-49d5-86df-b15c2f55106a] succeeded in 0.06079432299884502s: 'Sending SMS to 9876543210: Welcome to SCAI!'
```

### 3. Automated Unit Tests
```bash
python manage.py test contacts
```
Output:
```text
Ran 8 tests in 0.083s
OK
```
