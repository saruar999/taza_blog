from .base import BaseModel
from .users import User, CustomUserManager
from django.contrib.auth.models import Group


class AuthorFavoritePosts(BaseModel):
    post = User.models.ForeignKey('core.Posts', related_name='favorited_by', on_delete=User.models.CASCADE)

    author = User.models.ForeignKey('core.Author', related_name='author_favorite_posts', on_delete=User.models.CASCADE)


class CustomAuthorManager(CustomUserManager):

    def create_user(self, email, password, **extra_fields):
        return self.create_unverified_user(email, password, **extra_fields)


class Author(User):

    objects = CustomAuthorManager()

    favorite_posts = User.models.ManyToManyField('core.Posts',
                                                 through='AuthorFavoritePosts',
                                                 through_fields=['author', 'post'],
                                                 help_text="List of favorited posts")

    def assign_author_group(self):
        self.assign_group(name='author')

