from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactViewSet, LoginView

router = DefaultRouter()
router.register(r'contacts', ContactViewSet, basename='contact')

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('', include(router.urls)),
]
