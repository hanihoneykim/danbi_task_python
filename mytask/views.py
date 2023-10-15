from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from teams.models import Team
from tasks.models import Task
from subtasks.models import SubTask
from tasks.serializers import TaskSerializer


class MyTasks(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # 현재 사용자가 속한 팀 찾기
        user_teams = Team.objects.filter(members=request.user)

        # 해당 팀과 관련된 작업 가져오기
        tasks = Task.objects.filter(team__in=user_teams)

        # 해당 팀과 관련된 서브태스크 가져오기
        subtasks = SubTask.objects.filter(team__in=user_teams)

        # 서브태스크에 연결된 작업 가져오기
        subtask_tasks = Task.objects.filter(subtasks__in=subtasks)

        # 작업 및 서브태스크 직렬화
        task_serializer = TaskSerializer(tasks, many=True)
        subtask_task_serializer = TaskSerializer(subtask_tasks, many=True)

        return Response(
            {
                "tasks": task_serializer.data,
                "subtask_tasks": subtask_task_serializer.data,
            }
        )
