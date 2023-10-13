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
            "team_name",
        )
        read_only_fields = ("password",)

    def get_team_name(self, obj):
        teams = obj.team.all()
        if teams:
            team_names = [team.name for team in teams]
            return ", ".join(team_names) + "팀"
        else:
            return "No Team"


class IDUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)


class NameUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name",)
