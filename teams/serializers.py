from rest_framework import serializers
from .models import Team
from users.serializers import NameUserSerializer


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField(read_only=True)
    is_myteam = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = (
            "name",
            "members",
            "is_myteam",
        )

    def get_members(self, obj):
        members = obj.members.all()
        return [member.name for member in members]

    def get_is_myteam(self, obj):
        # 현재 요청을 보내고 있는 사용자
        current_user = self.context["request"].user
        # 팀에 속한 멤버 목록 가져오기
        members = obj.members.all()
        # 현재 사용자가 팀의 멤버인지 확인
        is_member = current_user in members
        return is_member


class NameTeamSerializer(serializers.ModelSerializer):
    # is_myteam = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = (
            "name",
            # "is_myteam",
        )


"""
    def get_is_myteam(self, obj):
        # 현재 요청을 보내고 있는 사용자
        current_user = self.context["request"].user
        # 팀에 속한 멤버 목록 가져오기
        members = obj.members.all()
        # 현재 사용자가 팀의 멤버인지 확인
        is_member = current_user in members
        return is_member
"""
