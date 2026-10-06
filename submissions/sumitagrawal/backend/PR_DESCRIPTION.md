# API Test Results

### 1. List Contacts (GET)
**Request:** `GET http://127.0.0.1:8000/api/contacts/`
**Status Code:** `200`
**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "name": "Eve Black",
      "phone": "7778889999",
      "email": "eve@example.com",
      "created_at": "2026-10-06T14:14:46.993346Z"
    },
    {
      "id": 4,
      "name": "David White",
      "phone": "4445556666",
      "email": "david@example.com",
      "created_at": "2026-10-06T14:14:46.993344Z"
    },
    {
      "id": 3,
      "name": "Charlie Brown",
      "phone": "1112223333",
      "email": "charlie@example.com",
      "created_at": "2026-10-06T14:14:46.993341Z"
    },
    {
      "id": 2,
      "name": "Bob Jones",
      "phone": "0987654321",
      "email": "bob@example.com",
      "created_at": "2026-10-06T14:14:46.993337Z"
    },
    {
      "id": 1,
      "name": "Alice Smith",
      "phone": "1234567890",
      "email": "alice@example.com",
      "created_at": "2026-10-06T14:14:46.993325Z"
    }
  ]
}
```

### 2. Filter Contacts by Email (GET)
**Request:** `GET http://127.0.0.1:8000/api/contacts/?email=alice@example.com`
**Status Code:** `200`
**Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Alice Smith",
      "phone": "1234567890",
      "email": "alice@example.com",
      "created_at": "2026-10-06T14:14:46.993325Z"
    }
  ]
}
```

### 3. Search Contacts by Name (GET)
**Request:** `GET http://127.0.0.1:8000/api/contacts/?search=Charlie`
**Status Code:** `200`
**Response:**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "name": "Charlie Brown",
      "phone": "1112223333",
      "email": "charlie@example.com",
      "created_at": "2026-10-06T14:14:46.993341Z"
    }
  ]
}
```

### 4. Pagination Page 2 (GET)
**Request:** `GET http://127.0.0.1:8000/api/contacts/?page=2`
**Status Code:** `404`
**Response:**
```json
{
  "detail": "Invalid page."
}
```

### 5. Create Contact (POST)
**Request:** `POST http://127.0.0.1:8000/api/contacts/`
**Body:** `{"name": "Frank White", "phone": "1231231234", "email": "frank@example.com"}`
**Status Code:** `201`
**Response:**
```json
{
  "id": 6,
  "name": "Frank White",
  "phone": "1231231234",
  "email": "frank@example.com",
  "created_at": "2026-10-06T14:16:14.436262Z"
}
```

### 6. Retrieve Contact (GET)
**Request:** `GET http://127.0.0.1:8000/api/contacts/6/`
**Status Code:** `200`
**Response:**
```json
{
  "id": 6,
  "name": "Frank White",
  "phone": "1231231234",
  "email": "frank@example.com",
  "created_at": "2026-10-06T14:16:14.436262Z"
}
```

### 7. Update Contact (PUT)
**Request:** `PUT http://127.0.0.1:8000/api/contacts/6/`
**Body:** `{"name": "Frank White Updated", "phone": "9999999999", "email": "frank@example.com"}`
**Status Code:** `200`
**Response:**
```json
{
  "id": 6,
  "name": "Frank White Updated",
  "phone": "9999999999",
  "email": "frank@example.com",
  "created_at": "2026-10-06T14:16:14.436262Z"
}
```

### 8. Delete Contact (DELETE)
**Request:** `DELETE http://127.0.0.1:8000/api/contacts/6/`
**Status Code:** `204`
**Response:**
```json

```

### 9. Create Contact - Validation Error (POST)
**Request:** `POST http://127.0.0.1:8000/api/contacts/`
**Body:** `{"name": "Invalid Phone", "phone": "123", "email": "invalid@example.com"}`
**Status Code:** `400`
**Response:**
```json
{
  "phone": [
    "Phone must be exactly 10 digits."
  ]
}
```
