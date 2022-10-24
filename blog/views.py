from core.views import CustomModelViewSet
from core.permissions import DjangoModelPermissions
from core.paginations import StandardResultsSetPagination
from .permissions import CanUpdateDeletePost
from .serializers import PostsSerializer, CommentSerializer, LikePostSerializer, FavoritePostSerializer
from .filters import PostsFilter

from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class PostViewSet(CustomModelViewSet):
    serializer_class = PostsSerializer
    queryset = PostsSerializer.Meta.model.objects.all().prefetch_related('tags')
    permission_classes = (DjangoModelPermissions, CanUpdateDeletePost)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PostsFilter
    pagination_class = StandardResultsSetPagination

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        if self.error_res is not None:
            return self.error_res

        post.views += 1
        post.save()
        return super().retrieve(request, *args, **kwargs)

    @action(methods=['post'],
            url_path='like_post',
            url_name='like-post',
            detail=True)
    def like_post(self, request, pk=None):
        post = self.get_object()
        if self.error_res is not None:
            return self.error_res

        serializer = LikePostSerializer(post, data=request.data, context={'request': request})
        return self.serialize_extra_action(serializer, message='done')

    @action(methods=['post'],
            url_path='favorite_post',
            url_name='favorite-post',
            detail=True)
    def favorite_post(self, request, pk=None):
        post = self.get_object()
        if self.error_res is not None:
            return self.error_res

        serializer = FavoritePostSerializer(post, data=request.data, context={'request': request})
        return self.serialize_extra_action(serializer, message='done')


class CommentViewSet(CustomModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        post_id = self.kwargs.get('pid')
        if self.action == 'list':
            return CommentSerializer.Meta.model.top_level_comments.filter(post_id=post_id)
        else:
            return CommentSerializer.Meta.model.objects.filter(post_id=post_id)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"post_id": self.kwargs.get('pid')})
        return context
