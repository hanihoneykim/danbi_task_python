from django.test import TestCase
from rest_framework.test import APITestCase
from . import models


class TestUsers(APITestCase):
    NAME = "단비"
    USERNAME = "danbi"

    def setUp(self):
        models.User.objects.create(
            name=self.NAME,
            username=self.USERNAME,
        )

    def test_all_users(self):
        response = self.client.get("/api/v1/users/")
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
            self.NAME,
        )
        self.assertEqual(
            data[0]["username"],
            self.USERNAME,
        )
