from django.db import models
from users.models import User


class Team(models.Model):

    """Team Model Definition"""

    name = models.CharField(
        max_length=15,
        blank=True,
        default="",
    )
    members = models.ManyToManyField(
        "users.User",
        related_name="team",
    )

    def __str__(self):
        return f"{self.name}팀"
