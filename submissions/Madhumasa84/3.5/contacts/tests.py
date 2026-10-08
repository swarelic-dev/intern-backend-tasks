from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from contacts.models import Contact


class AuthAndPermissionsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="securepassword123")
        self.token = Token.objects.create(user=self.user)

        self.contact = Contact.objects.create(
            name="John Doe",
            phone="9876543210",
            email="john.doe@example.com"
        )
        self.list_url = reverse('contact-list')
        self.detail_url = reverse('contact-detail', kwargs={'pk': self.contact.pk})
        self.login_url = reverse('auth-login')

    def test_get_contacts_unauthenticated_allowed(self):
        """GET /api/contacts/ must be accessible without authentication"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_contact_unauthenticated_allowed(self):
        """GET /api/contacts/<id>/ must be accessible without authentication"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_contacts_unauthenticated_denied(self):
        """POST /api/contacts/ without authentication must return 401 Unauthorized"""
        payload = {"name": "Anon User", "phone": "9876543210", "email": "anon@example.com"}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_contact_unauthenticated_denied(self):
        """DELETE /api/contacts/<id>/ without authentication must return 401 Unauthorized"""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_invalid_credentials(self):
        """POST /api/auth/login/ with wrong password returns 401"""
        response = self.client.post(self.login_url, {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)

    def test_login_missing_credentials(self):
        """POST /api/auth/login/ without username/password returns 400"""
        response = self.client.post(self.login_url, {"username": "testuser"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_valid_credentials_returns_token(self):
        """POST /api/auth/login/ with valid credentials returns token"""
        response = self.client.post(self.login_url, {"username": "testuser", "password": "securepassword123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"], self.token.key)
        self.assertEqual(response.data["username"], "testuser")

    @patch('contacts.views.send_welcome_sms.delay')
    def test_post_contacts_authenticated_succeeds(self, mock_delay):
        """POST /api/contacts/ with valid Token authorization creates contact and dispatches task"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        payload = {"name": "Auth User", "phone": "9876543210", "email": "auth@example.com"}
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Auth User")
        mock_delay.assert_called_once_with("9876543210")

    def test_delete_contact_authenticated_succeeds(self):
        """DELETE /api/contacts/<id>/ with valid Token authorization deletes contact"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Contact.objects.filter(pk=self.contact.pk).exists())
