from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contact
from .serializers import ContactSerializer
from .pagination import ContactPagination


class ContactViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet providing full CRUD operations for Contact model with:
    - Query parameter filtering (e.g. ?email=test@example.com) via DjangoFilterBackend
    - Search across name, email, and phone (e.g. ?search=John) via SearchFilter
    - Pagination with 5 results per page (e.g. ?page=2) via ContactPagination
    """
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    pagination_class = ContactPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['email', 'phone', 'name']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
