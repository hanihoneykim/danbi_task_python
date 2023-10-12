from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK
from .models import Task
from .serializers import TaskSerializer


class Tasks(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(
            tasks,
            many=True,
        )
        return Response(serializer.data, status=HTTP_200_OK)
