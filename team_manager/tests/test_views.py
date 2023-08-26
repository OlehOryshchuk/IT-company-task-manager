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


class PrivateWorkerTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.position = Position.objects.create(name="position")

        self.user = get_user_model().objects.create_user(
            username="test_username", password="test_1234", position=self.position
        )
        self.client.force_login(self.user)

        self.is_paginated_by = 5

    def test_receive_list_of_workers(self):
        for i in range(10):
            get_user_model().objects.create(
                username=f"worker{i}",
                password=f"worker123{i}",
                position=Position.objects.create(
                    name=f"Position{i}"
                )
            )

        response = self.client.get(WORKER_LIST)
        workers = get_user_model().objects.all()[:self.is_paginated_by]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["worker_list"]),
            list(workers)
        )
        self.assertTemplateUsed(response, "team_manager/worker_list.html")

    def test_receive_worker_by_username(self):
        get_user_model().objects.create(
            username="user1",
            password="user10987"
        )
        get_user_model().objects.create(
            username="user2",
            password="user20987"
        )

        response = self.client.get(WORKER_LIST, data={
            "username": "user2"
        })

        self.assertEqual(response.status_code, 200)
        worker_list = response.context["worker_list"]
        self.assertEqual(len(worker_list), 1)
        self.assertEqual(
            worker_list[0].username,
            "user2"
        )

    def test_display_all_workers_from_the_team(self):
        searched_worker = Team.objects.create(
            name="Team1",
            owner=self.user,
        )
        searched_worker.members.add(self.user.id)
        Team.objects.create(
            name="Team2",
            owner=self.user
        )

        response = self.client.get(WORKER_LIST, data={
            "team_members": searched_worker.id
        })

        self.assertEqual(response.status_code, 200)
        worker_list = response.context["worker_list"]
        self.assertEqual(len(worker_list), 1)
        self.assertEqual(
            worker_list[0].username,
            self.user.username
        )

    def test_view_own_detail_page_with_update_delete_actions(self):
        url = reverse("team_manager:worker-detail", args=[self.user.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, reverse("team_manager:worker-update", args=[self.user.id]))
        self.assertContains(response, reverse("team_manager:worker-delete", args=[self.user.id]))


