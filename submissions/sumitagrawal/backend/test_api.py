import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'
TOKEN = '06da2556207449bb6227aca31ec5dbadd1027108'
HEADERS = {'Authorization': f'Token {TOKEN}', 'Content-Type': 'application/json'}

results = ["# API Test Results\n"]

def add_result(title, res):
    results.append(f"### {title}")
    results.append(f"**Request:** `{res.request.method} {res.request.url}`")
    if res.request.body:
        results.append(f"**Body:** `{res.request.body.decode('utf-8') if isinstance(res.request.body, bytes) else res.request.body}`")
    results.append(f"**Status Code:** `{res.status_code}`")
    try:
        data = res.json()
        formatted = json.dumps(data, indent=2)
    except:
        formatted = res.text
    results.append(f"**Response:**\n```json\n{formatted}\n```\n")

# GET List Contacts
res = requests.get(f"{BASE_URL}/contacts/")
add_result("1. List Contacts (GET)", res)
contact_id = res.json()['results'][0]['id']

# GET Filter Contacts by Email
res = requests.get(f"{BASE_URL}/contacts/?email=alice@example.com")
add_result("2. Filter Contacts by Email (GET)", res)

# GET Search Contacts by Name
res = requests.get(f"{BASE_URL}/contacts/?search=Charlie")
add_result("3. Search Contacts by Name (GET)", res)

# GET Pagination
res = requests.get(f"{BASE_URL}/contacts/?page=2")
add_result("4. Pagination Page 2 (GET)", res)

# POST Create Contact (requires Auth)
payload = {"name": "Frank White", "phone": "1231231234", "email": "frank@example.com"}
res = requests.post(f"{BASE_URL}/contacts/", headers=HEADERS, json=payload)
add_result("5. Create Contact (POST)", res)
new_id = res.json().get('id')

if new_id:
    # GET Retrieve Contact
    res = requests.get(f"{BASE_URL}/contacts/{new_id}/")
    add_result("6. Retrieve Contact (GET)", res)

    # PUT Update Contact
    update_payload = {"name": "Frank White Updated", "phone": "9999999999", "email": "frank@example.com"}
    res = requests.put(f"{BASE_URL}/contacts/{new_id}/", headers=HEADERS, json=update_payload)
    add_result("7. Update Contact (PUT)", res)

    # DELETE Contact
    res = requests.delete(f"{BASE_URL}/contacts/{new_id}/", headers=HEADERS)
    add_result("8. Delete Contact (DELETE)", res)

# POST Create Contact with Invalid Phone
payload = {"name": "Invalid Phone", "phone": "123", "email": "invalid@example.com"}
res = requests.post(f"{BASE_URL}/contacts/", headers=HEADERS, json=payload)
add_result("9. Create Contact - Validation Error (POST)", res)

with open('PR_DESCRIPTION.md', 'w') as f:
    f.write('\n'.join(results))
