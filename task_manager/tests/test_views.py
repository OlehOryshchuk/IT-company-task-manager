from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from datetime import datetime
from taggit.models import Tag

from ..models import TaskType, Task, Project
from team_manager.models import Team


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

    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="Test")
        self.task = Task.objects.create(
            name="task_test",
            deadline=datetime.today().date(),
            task_type=self.task_type
        )

    def test_task_filter_page_is_login_required(self):
        response = self.client.get(TASK_FILTER)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/task/filter/")

    def test_task_list_page_is_login_required(self):
        response = self.client.get(TASK_LIST)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/tasks/")

    def test_task_create_page_is_login_required(self):
        response = self.client.get(TASK_CREATE)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/task/create/")

    def test_task_update_page_is_login_required(self):
        url = reverse("task_manager:task-update", args=[self.task.id])

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/task/task/{self.task.id}/update/"
        )

    def test_task_delete_page_is_login_required(self):
        url = reverse("task_manager:task-delete", args=[self.task.id])

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/task/task/{self.task.id}/delete/"
        )


class PrivateProjectViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="MainUser", password="Main1234"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="MainType")

        self.paginated = 5

    def test_task_list_page(self):
        for i in range(6):
            Task.objects.create(
                name=f"test{i}",
                deadline=datetime.today().date(),
                task_type=self.task_type,
                owner=self.user,
            )

        response = self.client.get(TASK_LIST)
        tasks = Task.objects.all()[:self.paginated]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.context["task_list"]),
            list(tasks)
        )
        self.assertTemplateUsed(response, "task_manager/task_list.html")

    def test_receive_test_by_name(self):
        test_1 = Task.objects.create(
                name=f"test_1",
                deadline=datetime.today().date(),
                task_type=self.task_type,
                owner=self.user,
            )
        searched_test = Task.objects.create(
                name=f"Searched",
                deadline=datetime.today().date(),
                task_type=TaskType.objects.create(name="searched"),
                owner=self.user,
            )

        response = self.client.get(TASK_LIST, {"name": searched_test.name})

        self.assertEqual(response.status_code, 200)
        task_list = response.context["task_list"]

        self.assertEqual(len(task_list), 1)
        self.assertEqual(
            task_list[0].name,
            searched_test.name
        )

    def test_receive_test_by_task_type(self):
        test_1 = Task.objects.create(
                name=f"test_1",
                deadline=datetime.today().date(),
                task_type=self.task_type,
                owner=self.user,
            )
        searched_test = Task.objects.create(
                name=f"Searched",
                deadline=datetime.today().date(),
                task_type=TaskType.objects.create(name="searched"),
                owner=self.user,
            )

        response = self.client.get(TASK_LIST, {"task_type": searched_test.task_type.id})

        self.assertEqual(response.status_code, 200)
        task_list = response.context["task_list"]

        self.assertEqual(len(task_list), 1)
        self.assertEqual(
            task_list[0].task_type,
            searched_test.task_type
        )

    def test_receive_test_by_task_tag(self):
        tag_1 = Tag.objects.create(name="task_1")
        searched_tag = Tag.objects.create(name="searched_tag")

        task_1 = Task.objects.create(
                name=f"task_1",
                deadline=datetime.today().date(),
                task_type=self.task_type,
                owner=self.user,
            )
        task_1.tags.add(tag_1)

        searched_test = Task.objects.create(
                name=f"Searched",
                deadline=datetime.today().date(),
                task_type=TaskType.objects.create(name="searched"),
                owner=self.user,
            )
        searched_test.tags.add(searched_tag)

        response = self.client.get(TASK_LIST, {"tags": searched_tag.name})

        self.assertEqual(response.status_code, 200)
        task_list = response.context["task_list"]

        self.assertEqual(len(task_list), 1)
        self.assertEqual(
            task_list[0].tags.first().name,
            searched_test.tags.first().name
        )

    def test_receive_test_by_task_tags_name(self):
        task_1 = Task.objects.create(
                name=f"task_1",
                deadline=datetime.today().date(),
                task_type=self.task_type,
                owner=self.user,
            )
        searched_test = Task.objects.create(
                name=f"Searched",
                deadline=datetime.today().date(),
                task_type=TaskType.objects.create(name="searched"),
                owner=self.user,
                is_completed=True,
            )

        response = self.client.get(TASK_LIST, {"is_completed": searched_test.is_completed})

        self.assertEqual(response.status_code, 200)
        task_list = response.context["task_list"]

        self.assertEqual(len(task_list), 1)
        self.assertEqual(
            task_list[0].name,
            searched_test.name
        )


class PublicProjectViewTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="MainUser", password="Main1234"
        )
        self.team = Team.objects.create(
            name="MainTeam",
            owner=self.user,
        )
        self.team.members.add(self.user)

        self.project = Project.objects.create(
            name="MainProejct",
            deadline=datetime.today().date(),
            owner=self.user,
        )
        self.project.teams.add(self.team)

    def test_project_list_page_is_login_required(self):
        response = self.client.get(PROJECT_LIST)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/task/projects/")

    def test_project_detail_page_is_login_required(self):
        url = reverse("task_manager:project-detail", args=[self.project.id])

        response = self.client.get(url)

        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(
            response,
            f"/accounts/login/?next=/task/project/{self.project.id}/detail")
