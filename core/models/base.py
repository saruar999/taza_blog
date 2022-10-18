from django.db import models


class BaseModel(models.Model):

    models = models

    created_at = models.DateTimeField(auto_now_add=True, help_text="When was this entry created")

    updated_at = models.DateTimeField(auto_now=True, help_text="When was this entry updated")

    created_by = models.ForeignKey('core.User',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='%(class)s_created_by',)

    updated_by = models.ForeignKey('core.User',
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='%(class)s_updated_by',)

    class Meta:
        abstract = True
        ordering = ['-id']

