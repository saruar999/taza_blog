from .views import RegisterView, AdminRegisterView, LoginView
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(prefix="author", viewset=RegisterView, basename='register-author')
router.register(prefix="admin", viewset=AdminRegisterView, basename='register-admin')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', include(router.urls))
]
