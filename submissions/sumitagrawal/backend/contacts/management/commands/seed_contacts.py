from django.core.management.base import BaseCommand
from contacts.models import Contact

class Command(BaseCommand):
    help = 'Seeds 5 dummy contacts'

    def handle(self, *args, **kwargs):
        contacts = [
            Contact(name='Alice Smith', phone='1234567890', email='alice@example.com'),
            Contact(name='Bob Jones', phone='0987654321', email='bob@example.com'),
            Contact(name='Charlie Brown', phone='1112223333', email='charlie@example.com'),
            Contact(name='David White', phone='4445556666', email='david@example.com'),
            Contact(name='Eve Black', phone='7778889999', email='eve@example.com'),
        ]
        Contact.objects.bulk_create(contacts)
        self.stdout.write(self.style.SUCCESS('Successfully seeded 5 contacts'))
