from rest_framework import serializers
from .models import SubTask
from teams.serializers import NameTeamSerializer


class SubTaskSerializer(serializers.ModelSerializer):
    team = NameTeamSerializer(read_only=True, many=True)

    class Meta:
        model = SubTask
        fields = (
            "id",
            "team",
            "is_complete",
            "created_at",
            "modified_at",
            "completed_date",
        )


class TinySubTaskSerializer(serializers.ModelSerializer):
    team = NameTeamSerializer(many=True)

    class Meta:
        model = SubTask
        fields = (
            "id",
            "team",
        )
