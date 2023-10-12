from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    created_user_name = serializers.SerializerMethodField(read_only=True)
    team_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "created_user_name",
            "team_name",
            "title",
            "content",
            "is_complete",
            "created_at",
            "modified_at",
            "completed_data",
        )

    def get_created_user_name(self, obj):
        if obj.created_user:
            return obj.created_user.name
        else:
            return None

    def get_team_name(self, obj):
        if obj.team:
            return f"{obj.team.name}팀"
        else:
            return None
