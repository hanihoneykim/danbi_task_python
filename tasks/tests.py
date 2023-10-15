from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from tasks.models import Task
from users.models import User
from teams.models import Team
from subtasks.models import SubTask


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


class TestTaskDetail(APITestCase):
    def setUp(self):
        # testuser 생성
        user = User.objects.create(
            username="test",
            name="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

        # test data 생성
        task = Task.objects.create(title="Task1")
        self.subtask = SubTask.objects.create(task=task)
        self.team1 = Team.objects.create(name="team1")
        team2 = Team.objects.create(name="team2")
        self.team_dicts = [
            {"name": "team1"},
            {"name": "team2"},
        ]
        self.subtask.team.set([self.team1, team2])
        self.team_names = list(self.team_dicts)

    def test_put_task(self):
        # 로그인
        self.client.force_login(
            self.user,
        )
        # 액세스 권한 설정 (예: IsAuthenticated)
        self.client.force_authenticate(user=self.user)

        team3 = Team.objects.create(name="team3")
        team_dicts = [
            {"name": "team1"},
            {"name": "team3"},
        ]
        self.subtask.team.set([self.team1, team3])
        self.team_names = list(team_dicts)

        team_names_str = "team1, team3"

        response = self.client.put(
            f"/api/v1/tasks/1",
            data={
                "subtasks": [
                    {
                        "team": team_names_str,
                        "is_complete": False,
                    }
                ]
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        data = response.json()

        # 이름 비교
        self.assertEqual(
            data[0]["name"],
            "team1",
        )


class TestTaskSubTask(APITestCase):
    def setUp(self):
        # testuser 생성
        user = User.objects.create(
            username="test",
            name="test",
        )
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_task_subtask(self):
        # test data 생성
        team1 = Team.objects.create(name="team1")
        team2 = Team.objects.create(name="team2")

        # 로그인
        self.client = Client()
        self.client.force_login(
            self.user,
        )
        new_subtask = SubTask.objects.create(
            task=Task.objects.create(title="task"),
        )
        new_subtask.team.set([team1, team2])
        new_subtask.save()
        print(new_subtask)

        response = self.client.post(
            "/api/v1/tasks/1/subtask",
            data={"team": ["team1", "team2"]},
            content_type="application/json",
        )
        data = response.json()
        print("DATA:", data)

        self.assertEqual(
            response.status_code,
            201,
        )
        self.assertEqual(
            data["task"],
            "task",
        )
