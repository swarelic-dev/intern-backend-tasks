from django.core.management.base import BaseCommand
from contacts.models import Contact


class Command(BaseCommand):
    help = 'Seed the database with 5 dummy contacts'

    def handle(self, *args, **options):
        contacts_data = [
            {
                'name': 'John Doe',
                'phone': '9876543210',
                'email': 'john.doe@example.com',
            },
            {
                'name': 'Jane Smith',
                'phone': '9123456780',
                'email': 'jane.smith@example.com',
            },
            {
                'name': 'Alice Johnson',
                'phone': '9234567891',
                'email': 'alice.johnson@example.com',
            },
            {
                'name': 'Bob Brown',
                'phone': '9345678902',
                'email': 'bob.brown@example.com',
            },
            {
                'name': 'Charlie Davis',
                'phone': '9456789013',
                'email': 'charlie.davis@example.com',
            },
        ]

        created_count = 0
        for item in contacts_data:
            contact, created = Contact.objects.get_or_create(
                email=item['email'],
                defaults={
                    'name': item['name'],
                    'phone': item['phone'],
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created contact: {contact.name} ({contact.phone})")
            else:
                self.stdout.write(f"Contact already exists: {contact.name}")

        self.stdout.write(self.style.SUCCESS(f"Successfully processed 5 contacts ({created_count} newly created)."))
