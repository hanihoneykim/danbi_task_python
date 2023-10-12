from django.db import models


class Team(models.Model):

    """Team Model Definition"""

    name = models.CharField(
        max_length=15,
        blank=True,
        default="",
    )

    def __str__(self):
        return f"{self.name}팀"
