from django.test import TestCase
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.urls import reverse
from datetime import datetime
from taggit.models import Tag

from ..models import TaskType, Task, Project
from team_manager.models import Team
from ..admin import TaskAdmin


class AdminSiteTest(TestCase):
    def setUp(self) -> None:
        self.admin_user = get_user_model().objects.create_superuser(
            username="test_username", password="test1234"
        )
        self.client.force_login(self.admin_user)

        self.task_type = TaskType.objects.create(name="MainTaskType")

    def test_admin_task_type_list_has_field_name(self):
        new_task_type = TaskType.objects.create(name="new_task-type")
        url = reverse("admin:task_manager_tasktype_changelist")

        response = self.client.get(url)

        self.assertContains(response, new_task_type.name)

    def test_task_type_admin_search_by_name(self):
        task_type1 = TaskType.objects.create(name="Bug")
        task_type2 = TaskType.objects.create(name="Feature")

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

    def test_admin_task_list_has_all_fields(self):
        new_task = Task.objects.create(
            name="new_task-type",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
            owner=self.admin_user,
        )

        url = reverse("admin:task_manager_task_changelist")

        response = self.client.get(url)

        self.assertContains(response, new_task.name)
        self.assertContains(response, new_task.description)
        self.assertContains(response, new_task.is_completed)
        self.assertIn("deadline", TaskAdmin(model=Task, admin_site=admin.site).list_display)
        self.assertContains(response, new_task.priority.capitalize())

    def test_task_admin_search_by_name(self):
        task1 = Task.objects.create(
            name="task_1",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
            owner=self.admin_user,
        )
        task2 = Task.objects.create(
            name="task_2",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
            owner=self.admin_user,
        )

        url = reverse("admin:task_manager_task_changelist")

        response = self.client.get(url, {"q": task1.name.lower()})

        changelist = response.context['cl']
        self.assertEqual(task1.name, changelist.queryset.first().name)
        self.assertNotIn(task2, changelist.queryset)

    def test_task_admin_filter_by_tag(self):
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")

        task1 = Task.objects.create(
            name="task_1",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
            owner=self.admin_user,
        )
        task2 = Task.objects.create(
            name="task_2",
            description="Task for testing",
            deadline=datetime.today().date(),
            task_type=self.task_type,
            owner=self.admin_user,
        )
        task1.tags.add(tag1)
        task2.tags.add(tag2)

        url = reverse("admin:task_manager_task_changelist")

        response = self.client.get(url, {"tags__tasks__id__exact": tag1.id})

        changelist = response.context['cl']
        self.assertEqual(task1, changelist.queryset.first())
        self.assertNotIn(task2, changelist.queryset.all())

    def test_admin_project_list_has_all_fields(self):
        new_team = Team.objects.create(name="newTeam", owner=self.admin_user)
        new_team.members.add(self.admin_user)
        new_project = Project.objects.create(
            name="new_task-type",
            description="Task for testing",
            deadline=datetime.today().date(),
            owner=self.admin_user,
        )

        url = reverse("admin:task_manager_project_changelist")

        response = self.client.get(url)

        self.assertContains(response, new_project.name)
        self.assertContains(response, new_project.description)
        self.assertContains(response, new_project.is_completed,)
        self.assertIn("deadline", TaskAdmin(model=Task, admin_site=admin.site).list_display)
        self.assertContains(response, new_project.priority.capitalize())

    def test_project_admin_search_by_name(self):
        project1 = Project.objects.create(
            name="project_1",
            description="Project for testing",
            deadline=datetime.today().date(),
            owner=self.admin_user,
        )
        project2 = Project.objects.create(
            name="project_2",
            description="Project for testing",
            deadline=datetime.today().date(),
            owner=self.admin_user,
        )

        url = reverse("admin:task_manager_project_changelist")

        response = self.client.get(url, {"q": project1.name.lower()})

        changelist = response.context['cl']
        self.assertEqual(project1.name, changelist.queryset.first().name)
        self.assertNotIn(project2, changelist.queryset)

    def test_project_admin_filter_by_tag(self):
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")

        project1 = Project.objects.create(
            name="project_1",
            description="Project for testing",
            deadline=datetime.today().date(),
            owner=self.admin_user,
        )
        project2 = Project.objects.create(
            name="project_2",
            description="Project for testing",
            deadline=datetime.today().date(),
            owner=self.admin_user,
        )
        project1.tags.add(tag1)
        project2.tags.add(tag2)

        url = reverse("admin:task_manager_project_changelist")

        response = self.client.get(url, {"tags__projects__id__exact": tag1.id})

        changelist = response.context['cl']
        self.assertEqual(project1, changelist.queryset.first())
        self.assertNotIn(project2, changelist.queryset.all())
