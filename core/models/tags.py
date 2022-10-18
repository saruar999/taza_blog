from .base import BaseModel


class Tags(BaseModel):

    label = BaseModel.models.CharField(max_length=40, help_text="Tag label (content)")
