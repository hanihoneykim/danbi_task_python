from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.status import HTTP_200_OK
from .models import Team
from .serializers import TeamSerializer


class Teams(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(
            teams,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data, status=HTTP_200_OK)
