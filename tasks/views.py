from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Task
from teams.models import Team
from subtasks.models import SubTask
from subtasks.serializers import SubTaskSerializer, TinySubTaskSerializer
from .serializers import TaskSerializer


class Tasks(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(
            tasks,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        task_serializer = TaskSerializer(data=request.data)
        if task_serializer.is_valid():
            task = task_serializer.save(create_user=request.user)
            team_name = request.data.get("team")
            try:
                team = Team.objects.get(name=team_name)
                task.team = team
                task.save()
            except Team.DoesNotExist:
                return Response(
                    {"error": f"팀 '{team_name}'을(를) 찾을 수 없음"}, status=HTTP_400_BAD_REQUEST
                )
            subtasks = SubTask.objects.filter(task=task)
            subtask_serializer = SubTaskSerializer(subtasks, many=True)
            return Response(
                {
                    "task": task_serializer.data,
                    "subtasks": subtask_serializer.data,
                },
                status=HTTP_201_CREATED,
            )
        else:
            return Response(task_serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskSerializer(
            task,
            context={"request": request},
        )
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task.create_user != request.user:
            raise PermissionDenied

        serializer = TaskSerializer(
            task,
            data=request.data,
            partial=True,
            context={"request": request},
        )

        if serializer.is_valid():
            # 업데이트하려는 Task의 Team 정보를 업데이트
            new_team = serializer.validated_data.get("team")
            if new_team:
                task.team = new_team
                task.save()

            # 받아온 SubTask의 Team 정보로 SubTasks를 업데이트
            subtask_data = request.data.get("subtasks", [])

            # SubTasks의 Team 정보 초기화
            task.subtasks.clear()  # 기존의 Team 정보를 모두 초기화합니다.

            # 각 SubTask의 "team" 필드 처리
            for subtask_info in subtask_data:
                team_list = subtask_info.get("team", [])
                for team_info in team_list:
                    team_name = team_info.get("name", None)
                    if team_name:
                        try:
                            # Team 객체 찾거나 생성
                            team, created = Team.objects.get_or_create(name=team_name)
                            task.subtasks.add(team)
                        except Team.DoesNotExist:
                            pass
            task.save()
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TaskSubTasks(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        task = self.get_object(pk)
        subtasks = SubTask.objects.filter(task=task)  # 해당 task에 속하는 모든 subtasks 가져오기
        serializer = SubTaskSerializer(
            subtasks,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request, pk):
        # Task 객체를 가져옵니다.
        task = self.get_object(pk)

        # 요청 데이터에서 "team" 필드의 문자열 리스트를 추출합니다.
        team_names = request.data.get("team", [])

        # Task와 관련된 새로운 SubTask를 생성합니다.
        subtask = SubTask.objects.create(task=task)

        # 각 팀 이름에 대해 반복합니다.
        for team_name in team_names:
            try:
                # 팀 이름으로 팀 객체를 데이터베이스에서 찾습니다.
                team = Team.objects.get(name=team_name)

                # SubTask와 팀을 연결하기 위해 add() 메서드를 사용합니다.
                subtask.team.add(team)
            except Team.DoesNotExist:
                # 팀이 존재하지 않는 경우, 에러를 반환합니다.
                return Response(
                    {"error": f"팀 '{team_name}'을(를) 찾을 수 없음"}, status=HTTP_404_NOT_FOUND
                )
        # SubTask 객체를 직렬화하고 클라이언트에 반환합니다.
        serializer = SubTaskSerializer(subtask, context={"request": request})
        return Response(serializer.data, status=HTTP_201_CREATED)
