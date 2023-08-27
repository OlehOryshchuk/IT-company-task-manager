from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime

from ..models import TaskType, Task, Project


class ModelsTest(TestCase):

    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="Bug")
        self.user = get_user_model().objects.create_superuser(
            username="test_username", password="test1234"
        )

    def test_task_type_string_representation(self):
        self.assertEqual(str(self.task_type), self.task_type.name)

    def test_task_string_representation(self):
        task = Task.objects.create(
            name="task_2",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
            owner=self.user,
        )
        self.assertEqual(str(task), task.name)

    def test_project_string_representation(self):
        project = Project.objects.create(
            name="project_1",
            description="Project for testing",
            deadline=datetime.today().date(),
            owner=self.user,
        )
        self.assertEqual(str(project), project.name)
