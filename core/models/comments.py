from .base import BaseModel


class Comments(BaseModel):

    post = BaseModel.models.ForeignKey('core.Posts', related_name='comments',
                                       help_text="the post where comment is placed",
                                       on_delete=BaseModel.models.CASCADE)

    body = BaseModel.models.CharField(max_length=2040, help_text="Body of comment (content)")

    level = BaseModel.models.IntegerField(default=0, help_text="level of depth if comment is nested")

    parent_comment = BaseModel.models.ForeignKey('self',
                                                 null=True,
                                                 on_delete=BaseModel.models.CASCADE,
                                                 help_text="Comment object which this comment replied to")

