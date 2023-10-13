from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import SubTask
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
