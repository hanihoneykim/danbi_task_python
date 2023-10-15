from django.db import models
from common.models import CommonModel


class SubTask(CommonModel):
    """Model Definition for SubTask"""

    team = models.ManyToManyField(
        "teams.Team",
        related_name="subtasks",
    )
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.SET_NULL,
        related_name="subtasks",
        null=True,
    )
