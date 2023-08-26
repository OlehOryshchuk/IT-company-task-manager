from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.urls import reverse

from ..models import Position, Worker, Team


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_username", password="test1234"
        )
        self.client.force_login(self.admin_user)

        self.position = Position.objects.create(name="Developer")

    def test_admin_position_list_has_position(self):
        url = reverse("admin:team_manager_position_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.position.name)

    def test_admin_position_search_by_position(self):
        Position.objects.create(name="QA")

        url = reverse("admin:team_manager_position_changelist")

        response = self.client.get(url, {"q": self.position.name.lower()})

        changelist = response.context['cl']
        self.assertIn(self.position, changelist.queryset)
