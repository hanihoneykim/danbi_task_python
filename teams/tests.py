from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestTeams(APITestCase):
    def test_all_teams(self):
        team = models.Team.objects.create(name="Team1")
        user1 = User.objects.create(username="user1", name="User1")
        user2 = User.objects.create(username="user2", name="User2")
        team.members.set([user1, user2])

        # team.members 확인
        member_names = list(team.members.values_list("name", flat=True))
        print("Member Names:", member_names)

        response = self.client.get("/api/v1/teams/")
        data = response.json()

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
            data[0]["name"],
            "Team1",
        )
        self.assertEqual(
            data[0]["members"],
            member_names,
        )
