from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from contacts.models import Contact


class ContactFilterSearchPaginationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('contact-list')

        # Create 12 contacts to thoroughly test pagination (5 per page)
        self.contacts = []
        for i in range(1, 13):
            contact = Contact.objects.create(
                name=f"User {i:02d}",
                phone=f"90000000{i:02d}",
                email=f"user{i:02d}@example.com"
            )
            self.contacts.append(contact)

        # Explicitly named contacts for filtering and searching
        self.special_contact = Contact.objects.create(
            name="Johnathan Special",
            phone="9123456789",
            email="special.john@example.com"
        )

    def test_filter_by_email(self):
        """GET /api/contacts/?email=special.john@example.com - filtering by email"""
        response = self.client.get(self.list_url, {'email': 'special.john@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "Johnathan Special")
        self.assertEqual(response.data['results'][0]['email'], "special.john@example.com")

    def test_search_by_name(self):
        """GET /api/contacts/?search=John - searching across contacts"""
        response = self.client.get(self.list_url, {'search': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], "Johnathan Special")

    def test_pagination_page_1(self):
        """GET /api/contacts/?page=1 - verify 5 results per page on page 1"""
        response = self.client.get(self.list_url, {'page': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 13)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNone(response.data['previous'])

    def test_pagination_page_2(self):
        """GET /api/contacts/?page=2 - verify 5 results on page 2"""
        response = self.client.get(self.list_url, {'page': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 13)
        self.assertEqual(len(response.data['results']), 5)
        self.assertIsNotNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])

    def test_pagination_page_3(self):
        """GET /api/contacts/?page=3 - verify remaining 3 results on page 3"""
        response = self.client.get(self.list_url, {'page': 3})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 13)
        self.assertEqual(len(response.data['results']), 3)
        self.assertIsNone(response.data['next'])
        self.assertIsNotNone(response.data['previous'])
