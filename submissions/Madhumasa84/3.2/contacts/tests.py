from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from contacts.models import Contact


class ContactAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.contact = Contact.objects.create(
            name="John Doe",
            phone="9876543210",
            email="john.doe@example.com"
        )
        self.list_url = reverse('contact-list')
        self.detail_url = reverse('contact-detail', kwargs={'pk': self.contact.pk})

    def test_list_contacts(self):
        """GET /api/contacts/ - list all contacts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "John Doe")

    def test_create_contact_valid(self):
        """POST /api/contacts/ - create contact with valid 10-digit phone"""
        payload = {
            "name": "Jane Smith",
            "phone": "9123456780",
            "email": "jane.smith@example.com"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Jane Smith")
        self.assertEqual(response.data['phone'], "9123456780")
        self.assertTrue(Contact.objects.filter(email="jane.smith@example.com").exists())

    def test_create_contact_invalid_phone_length(self):
        """POST /api/contacts/ - validation error when phone is not 10 digits"""
        payload = {
            "name": "Invalid Phone",
            "phone": "12345",
            "email": "invalid@example.com"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)
        self.assertEqual(response.data["phone"][0], "Phone number must be exactly 10 digits.")

    def test_create_contact_invalid_phone_non_digit(self):
        """POST /api/contacts/ - validation error when phone contains non-digits"""
        payload = {
            "name": "Non Digit Phone",
            "phone": "98765abcd0",
            "email": "nondigit@example.com"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)
        self.assertEqual(response.data["phone"][0], "Phone number must be exactly 10 digits.")

    def test_retrieve_contact(self):
        """GET /api/contacts/<id>/ - retrieve single contact"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "John Doe")
        self.assertEqual(response.data['phone'], "9876543210")

    def test_retrieve_nonexistent_contact(self):
        """GET /api/contacts/<id>/ - 404 for nonexistent contact"""
        url = reverse('contact-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_contact(self):
        """PUT /api/contacts/<id>/ - update existing contact"""
        payload = {
            "name": "John Updated",
            "phone": "9999999999",
            "email": "john.updated@example.com"
        }
        response = self.client.put(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "John Updated")
        self.assertEqual(response.data['phone'], "9999999999")
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "John Updated")

    def test_delete_contact(self):
        """DELETE /api/contacts/<id>/ - delete existing contact"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())
