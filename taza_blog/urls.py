"""taza_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from authentication.urls import urlpatterns as auth_urls
from authorization.urls import urlpatterns as authorization_urls
from user_management.urls import urlpatterns as user_urls
from blog.urls import urlpatterns as blog_urls

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include(auth_urls)),
    path('', include(authorization_urls)),
    path('', include(user_urls)),
    path('', include(blog_urls))
]

