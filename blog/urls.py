from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet


router = DefaultRouter()
router.register(prefix='posts', viewset=PostViewSet, basename='posts')

comment_router = DefaultRouter()
comment_router.register(prefix='comments', viewset=CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:pid>/', include(comment_router.urls))
]
