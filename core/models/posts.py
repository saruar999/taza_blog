from .base import BaseModel


class PostTags(BaseModel):

    post = BaseModel.models.ForeignKey('core.Posts', related_name='post_tags', on_delete=BaseModel.models.CASCADE)

    tag = BaseModel.models.ForeignKey('core.Tags', related_name='tag_posts', on_delete=BaseModel.models.CASCADE)


class Posts(BaseModel):

    title = BaseModel.models.CharField(max_length=255, help_text="Title of the post")

    body = BaseModel.models.CharField(max_length=4080, help_text="Body of the post")

    header_img = BaseModel.models.ImageField(help_text="Image to be placed at the top of blog post")

    views = BaseModel.models.IntegerField(help_text="number of views", default=0)

    likes = BaseModel.models.IntegerField(help_text="number of likes", default=0)

    post_author = BaseModel.models.ForeignKey('core.Author', help_text="The author of post",
                                              related_name='posts', on_delete=BaseModel.models.SET_NULL,
                                              null=True)

    tags = BaseModel.models.ManyToManyField('core.Tags', through='PostTags',
                                            through_fields=['post', 'tag'],
                                            help_text="tags of the post")
