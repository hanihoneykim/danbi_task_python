from django.db import models
from common.models import CommonModel


class SubTask(CommonModel):
    """Model Definition for SubTask"""

    team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        related_name="subtasks",
        null=True,
    )
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.SET_NULL,
        related_name="subtasks",
        null=True,
    )

    def __str__(self):
        return f"{self.task}의 SubTask: {self.team}"
