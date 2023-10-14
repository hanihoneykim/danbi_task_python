from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from tasks.models import Task
from users.models import User
from teams.models import Team


class TestTasks(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username="test",
            name="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_task(self):
        response = self.client.post("/api/v1/tasks/")
        self.assertEqual(
            response.status_code,
            403,
        )
        # 로그인
        self.client.force_login(
            self.user,
        )
        team1 = Team.objects.create(name="team1")
        new_task = Task.objects.create(
            create_user=self.user,
            team=team1,
            title="Test Task",
            content="Test Task",
        )

        response = self.client.post(
            "/api/v1/tasks/",
            data={
                "create_user": new_task.create_user.name,
                "team": new_task.team.name,
                "title": new_task.title,
                "content": new_task.content,
            },
        )
        data = response.json()
        print("DATA:", data)
        print(response)
        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertEqual(
            data["task"]["create_user"]["name"],
            "test",
        )
        self.assertEqual(
            data["task"]["title"],
            "Test Task",
        )
