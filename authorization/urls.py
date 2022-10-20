from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, PermissionViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(prefix='roles', viewset=GroupViewSet, basename='roles')
router.register(prefix='permissions', viewset=PermissionViewSet, basename='permissions')

urlpatterns = [
    path('', include(router.urls))
]