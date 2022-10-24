from .base import BaseModel
from .tags import Tags


class PostTags(BaseModel):

    post = BaseModel.models.ForeignKey('core.Posts', related_name='post_tags', on_delete=BaseModel.models.CASCADE)

    tag = BaseModel.models.ForeignKey('core.Tags', related_name='tag_posts', on_delete=BaseModel.models.CASCADE)


class Posts(BaseModel):

    title = BaseModel.models.CharField(max_length=255, help_text="Title of the post")

    body = BaseModel.models.CharField(max_length=4080, help_text="Body of the post")

    header_img = BaseModel.models.ImageField(upload_to="post_headers/",
                                             blank=True,
                                             null=True,
                                             help_text="Image to be placed at the top of blog post")

    views = BaseModel.models.IntegerField(help_text="number of views", default=0)

    likes = BaseModel.models.IntegerField(help_text="number of likes", default=0)

    post_author = BaseModel.models.ForeignKey('core.User', help_text="The author of post",
                                              related_name='posts', on_delete=BaseModel.models.SET_NULL,
                                              null=True)

    tags = BaseModel.models.ManyToManyField('core.Tags', through='PostTags',
                                            through_fields=['post', 'tag'],
                                            help_text="tags of the post")

    def __str__(self):
        return str(self.id) + " - " + self.body

    def add_tags(self, tags):
        for tag in tags:
            saved_tag, created = Tags.objects.get_or_create(label=tag)
            self.tags.add(saved_tag)

    @property
    def comment_count(self):
        return self.comments.count()
