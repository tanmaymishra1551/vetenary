from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FarmerViewSet, RegisterViewSet

router = DefaultRouter()
router.register('farmers', FarmerViewSet, basename='farmer')
router.register('auth', RegisterViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]
