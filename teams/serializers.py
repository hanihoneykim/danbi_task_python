from rest_framework import serializers
from .models import Team
from users.serializers import NameUserSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = (
            "name",
            "members",
        )

    def get_members(self, obj):
        members = obj.members.all()
        return [member.name for member in members]


class NameTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("name",)
