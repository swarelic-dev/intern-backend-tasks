from rest_framework import viewsets
from .models import Contact
from .serializers import ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet providing full CRUD operations for Contact model:
    - GET /api/contacts/ (list)
    - POST /api/contacts/ (create)
    - GET /api/contacts/<id>/ (retrieve)
    - PUT /api/contacts/<id>/ (update)
    - PATCH /api/contacts/<id>/ (partial_update)
    - DELETE /api/contacts/<id>/ (destroy)
    """
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
