from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contact
from .serializers import ContactSerializer
from .pagination import ContactPagination
from .tasks import send_welcome_sms


class ContactViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet providing full CRUD operations for Contact model:
    - Query parameter filtering (e.g. ?email=test@example.com)
    - Full text search (?search=John)
    - Pagination with 5 results per page
    - Asynchronous dispatch of send_welcome_sms task via Celery on contact creation
    """
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    pagination_class = ContactPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['email', 'phone', 'name']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']

    def perform_create(self, serializer):
        """
        Save the contact and asynchronously dispatch the send_welcome_sms Celery task.
        Mirrors the SCAI rules engine asynchronous dispatch pattern.
        """
        contact = serializer.save()
        send_welcome_sms.delay(contact.phone)
