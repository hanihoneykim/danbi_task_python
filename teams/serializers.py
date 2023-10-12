from rest_framework import serializers
from .models import Team


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
