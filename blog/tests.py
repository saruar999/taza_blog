from core.tests import CustomApiTestCase, DetailsTestCaseMixin, ListTestCaseMixin
from core.models import Posts, Comments
from core.helpers.randoms import generate_random_string


class UserPostListTestCase(CustomApiTestCase, ListTestCaseMixin):

    url = 'posts-list'
    model = Posts
    permission_list = ['add_posts', 'view_posts']
    request_body = {
        "title": generate_random_string(10),
        "body": generate_random_string(50),
        "tags": [
            "educational",
            "test"
        ]
    }

    def test_list_unauthorized(self):
        pass


class UserPostDetailTestCase(CustomApiTestCase, DetailsTestCaseMixin):

    url = 'posts-detail'
    model = Posts
    permission_list = ['add_posts', 'view_posts']
    request_body = {
        "title": generate_random_string(10),
        "body": generate_random_string(50),
        "tags": [
            "educational",
            "test"
        ]
    }

    def setUp(self) -> None:
        obj = self.model.objects.create(title="test post",
                                        body=generate_random_string(50),
                                        post_author_id=1)
        self.url_kwargs = {'pk': obj.id}

    def test_retrieve_unauthorized(self):
        pass

    def test_update_authorized(self):
        pass

    def test_delete_authorized(self):
        pass


class OwnerPostDetailTestCase(CustomApiTestCase, DetailsTestCaseMixin):

    url = 'posts-detail'
    model = Posts
    permission_list = ['change_posts', 'view_posts', 'delete_posts']
    request_body = {
        "title": generate_random_string(10),
        "body": generate_random_string(50),
        "tags": [
            "educational",
            "test"
        ]
    }

    def setUp(self) -> None:
        user = self.get_temp_user()
        obj = self.model(title="test post",
                        body=generate_random_string(50))
        obj.post_author = user
        obj.save()
        self.url_kwargs = {'pk': obj.id}
        self.login_with_permissions(custom_user=user, custom_password="123")

    def test_retrieve_unauthorized(self):
        pass

    def test_update_authorized(self):
        self._test_request(method='patch')

    def test_delete_authorized(self):
        self._test_request(method='delete')


class PostExtraActionTestCase(CustomApiTestCase):
    model = Posts
    permission_list = ['add_posts', 'view_posts', 'change_posts']
    obj = None
    author = None

    def setUp(self) -> None:
        obj = Posts.objects.create(title="test post",
                                   body=generate_random_string(50),
                                   post_author_id=1)
        self.url_kwargs = {'pk': obj.id}
        self.obj = obj
        self.author = self.get_temp_author()
        self.login_with_permissions(custom_user=self.author, custom_password='123')

    def test_favorite_post(self):
        # favorite
        self.url = 'posts-favorite-post'
        self._test_request(method='post', expected_status=200)  # Noqa
        self.obj.refresh_from_db()
        self.author.refresh_from_db()

        self.assertEqual(self.obj.favorite_posts.count(), 1)
        self.assertTrue(self.author.favorite_posts.filter(id=self.obj.id).exists())

        #unfavorite
        self._test_request(method='post', expected_status=200)  # Noqa
        self.obj.refresh_from_db()
        self.author.refresh_from_db()

        self.assertEqual(self.obj.favorite_posts.count(), 0)
        self.assertFalse(self.author.favorite_posts.filter(id=self.obj.id).exists())

    def test_like_post(self):
        # Like

        self.url = 'posts-like-post'
        self._test_request(method='post', expected_status=200)
        self.obj.refresh_from_db()
        self.author.refresh_from_db()

        self.assertEqual(self.obj.likes, 1)
        self.assertTrue(self.author.liked_posts.filter(id=self.obj.id).exists())

        # Unlike
        self._test_request(method='post', expected_status=200)
        self.obj.refresh_from_db()
        self.author.refresh_from_db()

        self.assertEqual(self.obj.likes, 0)
        self.assertFalse(self.author.liked_posts.filter(id=self.obj.id).exists())


class CommentListTestCase(CustomApiTestCase, ListTestCaseMixin):

    model = Comments
    permission_list = ['add_comments', 'view_comments']
    request_body = {
        "body": generate_random_string(30),
        "parent_comment": None
    }

    def setUp(self) -> None:
        obj = Posts.objects.create(title="test post",
                                    body=generate_random_string(50),
                                    post_author_id=1)
        self.reversed_url = f'/posts/{obj.id}/comments/'


    def test_list_unauthorized(self):
        pass


class CommentDetailTestCase(CustomApiTestCase, DetailsTestCaseMixin):

    model = Comments
    permission_list = ['change_comments', 'view_comments', 'delete_comments']
    request_body = {
        "body": generate_random_string(30),
        "parent_comment": None
    }

    def setUp(self) -> None:
        post = Posts.objects.create(title="test post",
                                    body=generate_random_string(50),
                                    post_author_id=1)

        obj = self.model.objects.create(body=generate_random_string(20),
                                        post_id=post.id,
                                        level=1,
                                        parent_comment=None)

        self.reversed_url = f'/posts/{post.id}/comments/{obj.id}/'

    def test_retrieve_unauthorized(self):
        pass


