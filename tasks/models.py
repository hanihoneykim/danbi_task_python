from django.db import models
from common.models import CommonModel


class Task(CommonModel):
    """Model Definition for Task"""

    created_user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
    )
    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
    )
    title = models.CharField(
        max_length=140,
        default="",
    )
    content = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.title
