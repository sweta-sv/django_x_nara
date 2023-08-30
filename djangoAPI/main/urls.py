from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MockItemViewSet

router = DefaultRouter()
router.register(r'items', MockItemViewSet, basename="mock-item")

urlpatterns = [
    path('', include(router.urls)),
]