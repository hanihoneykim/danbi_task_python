from django.db import models
from django.utils import timezone


class CommonModel(models.Model):

    """Common Model Definition"""

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_complete = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    def mark_as_complete(self):
        self.is_complete = True
        self.completed_date = timezone.now()
        self.save()

    class Meta:
        abstract = True
