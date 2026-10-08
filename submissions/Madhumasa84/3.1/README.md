# Exercise 3.1 — Django Setup & First Model

## Overview
This submission implements Exercise 3.1: setting up a fresh Django project with a `contacts` app, defining the `Contact` model, registering it in Django Admin, applying database migrations, and providing a custom management command to seed dummy contacts.

## Architecture & Structure
```
submissions/Madhumasa84/3.1/
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
    ├── tests.py
    ├── views.py
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── __init__.py
    └── management/
        ├── __init__.py
        └── commands/
            ├── __init__.py
            └── seed_contacts.py
```

## Features Implemented
1. **Django Project & App Setup**: Created Django project `project` and modular app `contacts` registered in `INSTALLED_APPS`.
2. **Contact Model**:
   - `name`: `CharField(max_length=150)`
   - `phone`: `CharField(max_length=20)`
   - `email`: `EmailField()`
   - `created_at`: `DateTimeField(auto_now_add=True)`
   - Standard string representation `__str__` returning `name (phone)`.
   - Meta ordering by `-created_at`.
3. **Django Admin Registration**:
   - `list_display = ('name', 'phone', 'email', 'created_at')`
   - `search_fields = ('name', 'phone', 'email')`
   - `list_filter = ('created_at',)`
   - `date_hierarchy = 'created_at'`
4. **Database Migrations**: Initial migration generated and applied cleanly for SQLite.
5. **Data Seeding Command**:
   - Command `python manage.py seed_contacts` seeds 5 contacts with valid data and idempotent handling via `get_or_create`.
6. **Automated Unit Tests**:
   - Verification of model creation, `__str__` formatting, admin registry, and management command execution.

## Verification & Testing
```bash
# Apply migrations
python manage.py migrate

# Run seed command
python manage.py seed_contacts

# Run test suite
python manage.py test contacts
```
