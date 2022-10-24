from .base import BaseModel
from .users import User, CustomUserManager
from django.contrib.auth.models import Group


class AuthorFavoritePosts(BaseModel):
    post = User.models.ForeignKey('core.Posts', related_name='favorited_by', on_delete=User.models.CASCADE)

    author = User.models.ForeignKey('core.Author', related_name='author_favorite_posts', on_delete=User.models.CASCADE)


class AuthorLikedPosts(BaseModel):

    post = User.models.ForeignKey('core.Posts', related_name='liked_by', on_delete=User.models.CASCADE)
    author = User.models.ForeignKey('core.Author', related_name='author_liked_posts', on_delete=User.models.CASCADE)


class CustomAuthorManager(CustomUserManager):

    def create_user(self, email, password, **extra_fields):
        return self.create_unverified_user(email, password, **extra_fields)


class Author(User):

    objects = CustomAuthorManager()

    favorite_posts = User.models.ManyToManyField('core.Posts',
                                                 related_name='favorite_posts',
                                                 through='AuthorFavoritePosts',
                                                 through_fields=['author', 'post'],
                                                 help_text="List of favorited posts")

    liked_posts = User.models.ManyToManyField('core.Posts',
                                              related_name='liked_posts',
                                              through='AuthorLikedPosts',
                                              through_fields=['author', 'post'],
                                              help_text="List of liked posts")

    def assign_author_group(self):
        self.assign_group(name='author')

    @property
    def author_id(self):
        return self.id

    @staticmethod
    def return_classified_user_from_request_user(user):
        author = Author.objects.get(pk=user.id)
        return author


