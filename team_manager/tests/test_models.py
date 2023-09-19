from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import Position, Team


class ModelsTest(TestCase):

    def setUp(self) -> None:
        self.position = Position.objects.create(name="developer")
        self.worker = get_user_model().objects.create_user(
            username="driver_username",
            password="driver_1234",
            first_name="driver_name",
            last_name="driver_last_name",
            position=self.position,
        )
        self.team = Team.objects.create(
            name="Team1",
            description="Team1 description",
            owner=self.worker
        )
        self.team.members.add(self.worker)

    def test_position_str(self):
        self.assertEqual(str(self.position), f"{self.position.name}")

    def test_worker_str(self):
        self.assertEqual(str(self.worker), f"{self.worker.username}")

    def test_team_str(self):
        self.assertEqual(str(self.team), f"{self.team.name}")
