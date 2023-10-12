from rest_framework import serializers
from .models import User


class TinyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "id",
        )


class UserSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "username",
            "team",
            "team_name",
        )
        read_only_fields = ("password",)

    def get_team_name(self, obj):
        if obj.team:
            return f"{obj.team.name}팀"
        else:
            return "No Team"
