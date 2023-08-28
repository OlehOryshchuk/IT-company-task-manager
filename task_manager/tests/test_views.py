from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from datetime import datetime

from ..models import TaskType, Task, Project


TASK_TYPE_CREATE = reverse_lazy("task_manager:task-type-create")

TASK_LIST = reverse_lazy("task_manager:task-list")
TASK_CREATE = reverse_lazy("task_manager:task-create")
TASK_FILTER = reverse_lazy("task_manager:task-filter")

PROJECT_LIST = reverse_lazy("task_manager:project-list")
PROJECT_CREATE = reverse_lazy("task_manager:project-create")


class PublicTaskTypeTest(TestCase):
    def test_create_task_type_login_required(self):
        response = self.client.get(TASK_TYPE_CREATE)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/task_type/create/")


class PrivateTaskType(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="MainUser", password="Main1234",
        )
        self.client.force_login(self.user)

    def test_view_create_task_type_page(self):

        post_response = self.client.post(TASK_TYPE_CREATE, data={"name": "Bug"})
        get_response = self.client.get(TASK_TYPE_CREATE)

        self.assertRedirects(
            post_response,
            reverse("task_manager:task-list"),
            target_status_code=200,
            status_code=302
        )
        self.assertTrue(TaskType.objects.last().name == "Bug")
        self.assertTemplateUsed(get_response, "task_manager/task_type_form.html")


class PublicTaskViewTest(TestCase):

    def test_task_filter_page_is_login_required(self):
        response = self.client.get(TASK_FILTER)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/task/filter/")

    def test_task_list_page_is_login_required(self):
        response = self.client.get(TASK_LIST)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/tasks/")

