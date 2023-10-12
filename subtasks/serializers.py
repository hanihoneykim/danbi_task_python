from rest_framework import serializers
from .models import SubTask


class SubTaskSerializer(serializers.ModelSerializer):
    team_names = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SubTask
        fields = (
            "id",
            "team_names",
            "is_complete",
            "created_at",
            "modified_at",
            "completed_data",
        )

    def get_team_names(self, obj):
        team_names = [str(team) for team in obj.team.all()]
        return ", ".join(team_names)
