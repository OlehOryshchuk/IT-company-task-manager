from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from datetime import datetime

from ..models import TaskType, Task, Project


TASK_TYPE_CREATE = reverse_lazy("task_manager:task-type-create")

TASK_LIST = reverse_lazy("task_manager:task-list")
TASK_CREATE = reverse_lazy("task_manager:task-create")

PROJECT_LIST = reverse_lazy("task_manager:project-list")
PROJECT_CREATE = reverse_lazy("task_manager:project-create")


class PublicTaskTypeTest(TestCase):
    def test_create_task_type_login_required(self):
        response = self.client.get(TASK_TYPE_CREATE)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/task_type/create/")
