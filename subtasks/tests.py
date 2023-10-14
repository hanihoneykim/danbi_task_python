from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from . import models
from teams.models import Team
from tasks.models import Task


class TestSubTasks(APITestCase):
    def test_all_subtasks(self):
        task = Task.objects.create(title="Task1")
        subtask = models.SubTask.objects.create(task=task)
        team1 = Team.objects.create(name="team1")
        team2 = Team.objects.create(name="team2")
        team_dicts = [
            {"name": "team1"},
            {"name": "team2"},
        ]
        subtask.team.set([team1, team2])

        # team.members 확인
        team_names = list(team_dicts)
        # print("Team Names:", team_names)

        response = self.client.get("/api/v1/subtasks/")
        data = response.json()
        # print(data)

        self.assertEqual(
            response.status_code,
            200,
            "status code isn't 200",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["team"],
            team_names,
        )


class TestSubtaskDetail(APITestCase):
    def setUp(self):
        self.client = APIClient()
        # 다음 두 줄로 request 객체 생성 및 user 설정
        from django.contrib.auth import get_user_model

        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            name="testuser",
        )
        self.client.force_authenticate(user=self.user)

        task = Task.objects.create(title="Task1")
        self.subtask = models.SubTask.objects.create(task=task)
        self.team1 = Team.objects.create(name="team1")
        team2 = Team.objects.create(name="team2")
        self.team_dicts = [
            {"name": "team1"},
            {"name": "team2"},
        ]
        self.subtask.team.set([self.team1, team2])

        # team.members 확인
        self.team_names = list(self.team_dicts)
        # print("Team Names:", self.team_names)

    def test_subtask_not_found(self):
        response = self.client.get("/api/v1/subtasks/2")
        self.assertEqual(response.status_code, 404)

    def test_get_subtask(self):
        response = self.client.get("/api/v1/subtasks/1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("get_data:", data)

        # team_dicts 리스트에서 첫 번째 팀의 이름 추출
        expected_team_name = self.team_dicts[0]["name"]

        # 응답 데이터에서도 첫 번째 팀의 이름 추출
        actual_team_name = data["team"][0]["name"]

        # 이름 비교
        self.assertEqual(
            expected_team_name,
            actual_team_name,
        )

    def test_put_subtask(self):
        team3 = Team.objects.create(name="team3")
        team3.members.set([self.user])
        team_dicts = [
            {"name": "team1"},
            {"name": "team3"},
        ]
        self.subtask.team.set([self.team1, team3])

        # team.members 확인
        self.team_names = list(team_dicts)
        print("Team Names:", self.team_names)

        team_names_str = "team1, team3"

        response = self.client.put(
            f"/api/v1/subtasks/1",
            data={
                "team": team_names_str,
            },
        )

        print(response)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        print("Data:", data)

        # team_dicts 리스트에서 첫 번째 팀의 이름 추출
        expected_team_name = team_dicts[0]["name"]

        # 응답 데이터에서도 첫 번째 팀의 이름 추출
        actual_team_name = data["team"][0]["name"]

        # 이름 비교
        self.assertEqual(
            expected_team_name,
            actual_team_name,
        )

    def test_delete_subtask(self):
        response = self.client.delete("/api/v1/subtasks/1")
        self.assertEqual(response.status_code, 204)
