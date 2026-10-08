from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from contacts.models import Contact
from contacts.tasks import send_welcome_sms


class CeleryTaskTests(TestCase):
    def test_send_welcome_sms_task_direct(self):
        """Test direct invocation of send_welcome_sms task"""
        result = send_welcome_sms("9876543210")
        self.assertEqual(result, "Sending SMS to 9876543210: Welcome to SCAI!")

    @patch('contacts.views.send_welcome_sms.delay')
    def test_post_contact_dispatches_task(self, mock_delay):
        """POST /api/contacts/ should asynchronously dispatch send_welcome_sms.delay(phone)"""
        client = APIClient()
        url = reverse('contact-list')
        payload = {
            "name": "Celery User",
            "phone": "9876543210",
            "email": "celery.user@example.com"
        }
        response = client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_delay.assert_called_once_with("9876543210")


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
        self.assertEqual(response.data['count'], 1)

    @patch('contacts.views.send_welcome_sms.delay')
    def test_create_contact_valid(self, mock_delay):
        """POST /api/contacts/ - create contact with valid 10-digit phone and verify task dispatched"""
        payload = {
            "name": "Jane Smith",
            "phone": "9123456780",
            "email": "jane.smith@example.com"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_delay.assert_called_once_with("9123456780")

    def test_create_contact_invalid_phone(self):
        """POST /api/contacts/ - validation error when phone is not 10 digits"""
        payload = {
            "name": "Invalid Phone",
            "phone": "12345",
            "email": "invalid@example.com"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_contact(self):
        """GET /api/contacts/<id>/ - retrieve single contact"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_contact(self):
        """PUT /api/contacts/<id>/ - update existing contact"""
        payload = {
            "name": "John Updated",
            "phone": "9999999999",
            "email": "john.updated@example.com"
        }
        response = self.client.put(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_contact(self):
        """DELETE /api/contacts/<id>/ - delete existing contact"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
