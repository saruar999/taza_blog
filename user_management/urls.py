from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, AdminViewSet
from django.urls import path, include


router = DefaultRouter()

router.register(prefix='users', viewset=AuthorViewSet, basename='users')
router.register(prefix='admins', viewset=AdminViewSet, basename='admins')

urlpatterns = [
    path('', include(router.urls))
]
