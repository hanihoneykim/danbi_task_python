from rest_framework import serializers
from .models import Task
from subtasks.models import SubTask
from subtasks.serializers import TinySubTaskSerializer
from users.serializers import IDUserSerializer, NameUserSerializer
from teams.serializers import NameTeamSerializer


class TaskSerializer(serializers.ModelSerializer):
    subtasks = TinySubTaskSerializer(many=True, read_only=True)
    create_user = NameUserSerializer(read_only=True)
    team = NameTeamSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "create_user",
            "team",
            "title",
            "content",
            "is_complete",
            "created_at",
            "modified_at",
            "completed_date",
            "subtasks",
        )

    def get_subtasks(self, obj):
        # SubTask 정보 가져오기
        subtasks = SubTask.objects.filter(task=obj)
        if subtasks.exists():
            subtask_serializer = TinySubTaskSerializer(subtasks, many=True)
            return subtask_serializer.data
        else:
            return []
