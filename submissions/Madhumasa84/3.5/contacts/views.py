from django.contrib.auth import authenticate
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Contact
from .serializers import ContactSerializer
from .pagination import ContactPagination
from .tasks import send_welcome_sms


class ContactViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet providing full CRUD operations for Contact model:
    - GET /api/contacts/ and GET /api/contacts/<id>/ are publicly accessible without authentication.
    - POST /api/contacts/ and DELETE /api/contacts/<id>/ require token authentication (IsAuthenticated).
    - Query parameter filtering, search, and pagination are supported.
    - Dispatches send_welcome_sms task asynchronously upon contact creation.
    """
    queryset = Contact.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    pagination_class = ContactPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['email', 'phone', 'name']
    search_fields = ['name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        """
        Publicly allow read actions (list, retrieve); require authentication for write actions (create, destroy, update).
        """
        if self.action in ['list', 'retrieve'] or self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Save the contact and asynchronously dispatch the send_welcome_sms Celery task.
        """
        contact = serializer.save()
        send_welcome_sms.delay(contact.phone)


class LoginView(APIView):
    """
    Endpoint at /api/auth/login/ that returns an authentication token for valid credentials.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Both username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)
        if not user:
            return Response(
                {'error': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        }, status=status.HTTP_200_OK)
