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

    def __str__(self):
        team_names = ", ".join([str(team) for team in self.team.all()])
        return f"{self.task}의 SubTask: {team_names}"
