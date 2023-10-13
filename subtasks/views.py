from django.db import transaction
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import SubTask
from teams.models import Team
from .serializers import SubTaskSerializer


class SubTasks(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        subtasks = SubTask.objects.all()
        serializer = SubTaskSerializer(
            subtasks,
            context={"request": request},
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)


class SubTaskDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        subtask = self.get_object(pk)
        serializer = SubTaskSerializer(
            subtask,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        subtask = self.get_object(pk)
        user = request.user
        team_members = subtask.team.all().values_list("members", flat=True)
        if user.id not in team_members:
            raise PermissionDenied("You do not have permission to edit this SubTask.")
        serializer = SubTaskSerializer(
            subtask,
            data=request.data,
            partial=True,
            context={"request": request},
        )
        if serializer.is_valid():
            # is_complete가 True로 설정된 경우 completed_date를 현재 시간으로 업데이트
            if request.data.get("is_complete") is True:
                subtask.is_complete = True
                subtask.completed_date = timezone.now()

            if "team" in request.data:
                team_names = request.data["team"]
                # 기존 team 값 초기화
                subtask.team.clear()
                # 새로운 team 이름을 사용하여 추가
                for team_name in team_names:
                    try:
                        team = Team.objects.get(name=team_name)
                        subtask.team.add(team)
                    except Team.DoesNotExist:
                        # 존재하지 않는 팀 이름에 대한 처리
                        pass

            subtask.save()
            serializer = SubTaskSerializer(subtask)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subtask = self.get_object(pk)
        if subtask.user != request.user:
            raise PermissionDenied
        if subtask.is_complete:
            return Response({"주의": "완료된 하위과제는 삭제할 수 없습니다."}, status=HTTP_400_BAD_REQUEST)
        subtask.delete()
        return Response(status=HTTP_204_NO_CONTENT)
