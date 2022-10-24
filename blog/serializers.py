from rest_framework import serializers
from core.models import Posts, Comments, Author


class CommentSerializer(serializers.ModelSerializer):

    post = serializers.PrimaryKeyRelatedField(read_only=True)
    parent_comment = serializers.PrimaryKeyRelatedField(queryset=Comments.objects.all(),
                                                        allow_null=True)
    child_comments = serializers.SerializerMethodField(method_name='get_child_comments')

    @staticmethod
    def get_child_comments(obj):
        queryset = Comments.objects.filter(parent_comment=obj.id, level=obj.level+1)
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Comments
        fields = (
            'id', 'post', 'body', 'level', 'parent_comment', 'created_at', 'created_by', 'child_comments',
            'parent_comment'
        )
        extra_kwargs = {
            'level': {
                'read_only': True,
            },
        }

    def create(self, validated_data):

        post_id = self.context.get('post_id')
        request = self.context.get('request')

        parent_comment = validated_data.get('parent_comment')

        if parent_comment is not None:
            level = parent_comment.level + 1
        else:
            level = 1

        post = Posts.objects.get(pk=post_id)

        comment = Comments(**validated_data,
                           post_id=post_id,
                           level=level,
                           created_by=request.user,
                           updated_by=request.user)
        comment.save()
        post.comments.add(comment)
        post.save()
        return comment


class PostTopCommentsSerializer(serializers.ModelSerializer):

    has_replies = serializers.SerializerMethodField(method_name='check_has_replies')

    @staticmethod
    def check_has_replies(obj):
        return Comments.objects.filter(parent_comment=obj).exists()

    class Meta:
        model = Comments
        fields = (
            'id', 'body', 'created_at', 'created_by', 'has_replies',
        )
        extra_kwargs = {
            'level': {
                'read_only': True,
            },
        }


class PostsSerializer(serializers.ModelSerializer):

    tags = serializers.ListSerializer(child=serializers.CharField(max_length=40, min_length=2), min_length=1)
    comments = serializers.SerializerMethodField(method_name='get_top_level_comments')
    comment_count = serializers.SerializerMethodField(method_name='get_comment_count')

    class Meta:
        model = Posts
        exclude = ('updated_by', 'created_by', )
        extra_kwargs = {
            'views': {
                'read_only': True,
            },
            'likes': {
                'read_only': True,
            },
            'post_author': {
                'read_only': True,
            },
        }

    def create(self, validated_data):

        tags = validated_data.pop('tags')

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        instance = self.Meta.model(**validated_data)
        instance.post_author = user
        instance.save()
        instance.add_tags(tags)

        return instance

    def update(self, instance, validated_data):

        tags = validated_data.pop('tags')

        instance.tags.clear()
        instance.add_tags(tags)
        return super().update(instance, validated_data)

    @staticmethod
    def get_top_level_comments(obj):
        queryset = Comments.top_level_comments.filter(post_id=obj.id)
        serializer = PostTopCommentsSerializer(queryset, many=True)
        return serializer.data

    @staticmethod
    def get_comment_count(obj):
        return obj.comment_count


class LikePostSerializer(serializers.Serializer):

    def update(self, instance, validated_data):

        author = Author.return_classified_user_from_request_user(user=self.context.get('request').user)

        if author.liked_posts.filter(id=instance.id).exists():
            author.liked_posts.remove(instance)
            instance.likes -= 1
        else:
            author.liked_posts.add(instance)
            instance.likes += 1

        author.save()
        instance.save()
        return instance

    def create(self, validated_data):
        pass


class FavoritePostSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        author = Author.return_classified_user_from_request_user(user=self.context.get('request').user)

        if author.favorite_posts.filter(id=instance.id).exists():
            author.favorite_posts.remove(instance)
        else:
            author.favorite_posts.add(instance)

        author.save()
        return instance

