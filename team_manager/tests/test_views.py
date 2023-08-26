from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse

from ..models import Position, Team

POSITION_LIST = reverse_lazy("team_manager:position-list")

WORKER_LIST = reverse_lazy("team_manager:worker-list")
CREATE_WORKER = reverse_lazy("team_manager:worker-create")

TEAM_LIST = reverse_lazy("team_manager:team-list")
CREATE_TEAM = reverse_lazy("team_manager:team-create")


class PublicPositionTest(TestCase):
    def test_position_login_required(self):
        response = self.client.get(POSITION_LIST)

        self.assertNotEqual(response.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234"
        )
        self.client.force_login(self.user)

        self.is_paginated_by = 5

    def test_receive_list_of_position(self):
        for i in range(10):
            Position.objects.create(
                name=f"TestName{i}"
            )

        response = self.client.get(POSITION_LIST)
        positions = Position.objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["position_list"]),
            list(positions)
        )
        self.assertTemplateUsed(response, "team_manager/position_list.html")

    def test_receive_manufacturers_by_search_bar(self):
        Position.objects.create(name="Position1")
        Position.objects.create(name="Position2")
        searched = Position.objects.create(name="Position3")

        response = self.client.get(POSITION_LIST, data={
            "name": searched.name
        })

        self.assertEqual(response.status_code, 200)
        position_list = response.context["position_list"]
        self.assertEqual(len(position_list), 1)
        self.assertEqual(
            position_list[0].name,
            searched.name
        )


class PublicWorkerTest(TestCase):
    def test_worker_login_required(self):

        response = self.client.get(WORKER_LIST)

        self.assertNotEqual(response.status_code, 200)

