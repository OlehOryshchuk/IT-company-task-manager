from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime, timedelta
from ..models import TaskType, Task, Project
from team_manager.models import Team


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_username", password="test1234"
        )
        self.client.force_login(self.admin_user)

    def test_admin_task_type_list_has_field_name(self):
        new_task_type = TaskType.objects.create(name="new_task-type")
        url = reverse("admin:task_manager_tasktype_changelist")

        response = self.client.get(url)

        self.assertContains(response, new_task_type.name)

    def test_task_type_admin_search_by_name(self):
        task_type1 = TaskType.objects.create(name="Bug")
        task_type2 = TaskType.objects.create(name="Bug")

        url = reverse("admin:task_manager_tasktype_changelist")

        response = self.client.get(url, {"q": task_type1.name.lower()})

        changelist = response.context['cl']
        self.assertEqual(task_type1.name, changelist.queryset.first().name)
        self.assertNotIn(task_type2, changelist.queryset)

    def test_task_type_admin_filter_by_name(self):
        task_type1 = TaskType.objects.create(name="Bug")
        task_type2 = TaskType.objects.create(name="Feature")

        url = reverse("admin:task_manager_tasktype_changelist")

        response = self.client.get(url, {"name__exact": task_type1.name})

        changelist = response.context['cl']
        self.assertEqual(task_type1.name, changelist.queryset.first().name)
        self.assertNotIn(task_type2, changelist.queryset)
