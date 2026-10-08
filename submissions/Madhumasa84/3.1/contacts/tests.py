from django.test import TestCase
from django.core.management import call_command
from django.contrib import admin
from contacts.models import Contact


class ContactModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="Bruce Wayne",
            phone="9876543210",
            email="bruce@wayne.com"
        )

    def test_contact_str(self):
        self.assertEqual(str(self.contact), "Bruce Wayne (9876543210)")

    def test_contact_fields(self):
        self.assertEqual(self.contact.name, "Bruce Wayne")
        self.assertEqual(self.contact.phone, "9876543210")
        self.assertEqual(self.contact.email, "bruce@wayne.com")
        self.assertIsNotNone(self.contact.created_at)

    def test_admin_registration(self):
        self.assertIn(Contact, admin.site._registry)


class SeedContactsCommandTest(TestCase):
    def test_seed_contacts_command(self):
        Contact.objects.all().delete()
        self.assertEqual(Contact.objects.count(), 0)
        call_command('seed_contacts')
        self.assertEqual(Contact.objects.count(), 5)
