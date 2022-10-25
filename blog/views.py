from core.views import CustomModelViewSet
from core.permissions import DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAuthor
from core.paginations import StandardResultsSetPagination
from .permissions import CanUpdateDeletePost
from .serializers import PostsSerializer, CommentSerializer, LikePostSerializer, FavoritePostSerializer
from .filters import PostsFilter, AdminPostsFilter, CustomFilterBackend

from rest_framework.decorators import action


class PostViewSet(CustomModelViewSet):
    queryset = PostsSerializer.Meta.model.objects.all().prefetch_related('tags', 'post_author', 'comments')
    serializer_class = PostsSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, CanUpdateDeletePost)
    filter_backends = (CustomFilterBackend,)
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
            detail=True,
            permission_classes=(DjangoModelPermissions, IsAuthor,))
    def like_post(self, request, pk=None):
        post = self.get_object()
        if self.error_res is not None:
            return self.error_res

        serializer = LikePostSerializer(post, data=request.data, context={'request': request})
        return self.serialize_extra_action(serializer, message='done')

    @action(methods=['post'],
            url_path='favorite_post',
            url_name='favorite-post',
            detail=True,
            permission_classes=(DjangoModelPermissions, IsAuthor,))
    def favorite_post(self, request, pk=None):
        post = self.get_object()
        if self.error_res is not None:
            return self.error_res

        serializer = FavoritePostSerializer(post, data=request.data, context={'request': request})
        return self.serialize_extra_action(serializer, message='done')


class CommentViewSet(CustomModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (DjangoModelPermissionsOrAnonReadOnly, )

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
