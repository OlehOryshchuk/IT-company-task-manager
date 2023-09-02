from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError

from ..form import (
    TaskFilterForm,
    TaskSearchForm,
    TaskCreateForm,
    TaskChangeStatusForm,

    ProjectCreateForm,

    valid_deadline
)
from ..models import TaskType, Task, Project
from team_manager.models import Team


class TaskFormTest(TestCase):
    def setUp(self) -> None:
        self.filter_form = TaskFilterForm()
        self.user = get_user_model().objects.create(
            username="testuser", password="test123"
        )
        self.task_type = TaskType.objects.create(name="main_task_type")
        self.change_status_form = TaskChangeStatusForm(user=self.user)

    def test_filter_form_empty_label_and_required_should_be_false(self):
        self.assertEqual(
            self.filter_form.fields["task_type"].empty_label,
            "Filter by task type"
        )
        self.assertTrue(
            self.filter_form.fields["task_type"].required is False
        )
        self.assertTrue(
            self.filter_form.fields["is_completed"].required is False
        )

    def test_filter_form_field_task_type(self):
        TaskType.objects.create(name="bug")
        TaskType.objects.create(name="feature")

        filter_form = TaskFilterForm()

        self.assertEqual(
            list(filter_form.fields["task_type"].queryset.all()),
            list(TaskType.objects.all())
        )

    def test_search_form_field_name(self):
        search_form = TaskSearchForm()
        rendered_html = search_form.as_p()

        self.assertEqual(search_form.fields["name"].required, False)
        self.assertEqual(search_form.fields["name"].label, "")
        self.assertIn('placeholder="Search by task name"', rendered_html)

    def test_create_form_valid_data(self):
        form_data = {
            "name": "Test Task",
            "description": "This is a test task",
            "deadline": datetime.today().date(),
            "priority": "high",
            "task_type": self.task_type.id,
            "owner": self.user.id,
            "is_completed": True,
        }

        form = TaskCreateForm(data=form_data, user=self.user)
        print(form.errors)
        self.assertTrue(form.is_valid())

    def test_create_form_invalid_data(self):
        form_data = {
            "name": "Test Task",
            "priority": "high",
        }

        form = TaskCreateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_create_form_field_assignees(self):
        new_team = Team.objects.create(
            name="NewTeam", owner=self.user
        )
        user2 = get_user_model().objects.create(
            username="user2",
            password="user2123"
        )
        user3 = get_user_model().objects.create(
            username="user3",
            password="user3123"
        )
        user4 = get_user_model().objects.create(
            username="user4",
            password="user4123"
        )

        new_team.members.add(user2, user3, self.user)

        form_data = {
            "name": "Test Task",
            "description": "This is a test task",
            "deadline": datetime.today().date(),
            "priority": "high",
            "task_type": self.task_type.id,
            "owner": self.user.id,
            "is_completed": True,
        }

        create_form = TaskCreateForm(user=self.user, data=form_data)

        self.assertTrue(create_form.is_valid())
        create_form.save()

# user4 not supposed to be in assignees.queryset because he is not in same team
        self.assertEqual(
            list(create_form.fields["assignees"].queryset),
            [self.user, user2, user3]
        )
        self.assertTrue(user4 not in create_form.fields["assignees"].queryset)

    def test_change_status_form_fields_and_their_attributes(self):
        self.assertTrue(self.change_status_form.fields.get('assignees'))
        self.assertTrue(self.change_status_form.fields.get('is_completed'))
        self.assertTrue(
            self.change_status_form.fields["assignees"].required is False
        )
        self.assertTrue(
            self.change_status_form.fields["is_completed"].required is False
        )

    def test_change_status_form_field_assignees(self):
        task = Task.objects.create(
            name="task_name",
            deadline=datetime.today().date(),
            task_type=self.task_type,
            owner=self.user,
        )
        new_team = Team.objects.create(
            name="NewTeam", owner=self.user
        )
        user2 = get_user_model().objects.create(
            username="user2",
            password="user2123"
        )
        user3 = get_user_model().objects.create(
            username="user3",
            password="user3123"
        )
        user4 = get_user_model().objects.create(
            username="user4",
            password="user4123"
        )

        new_team.members.add(user2, user3, self.user)

        form_data = {
            "assignees": [self.user.id, user2.id],
            "is_completed": True,
        }

        changed_task = TaskChangeStatusForm(
            instance=task,
            user=self.user,
            data=form_data
        )

        self.assertTrue(changed_task.is_valid())
        changed_task.save()

# user4 not supposed to be in assignees.queryset because he is not in same team
        self.assertEqual(
            list(changed_task.fields["assignees"].queryset),
            [self.user, user2, user3]
        )
        self.assertEqual(
            list(task.assignees.all()),
            [self.user, user2]
        )
        self.assertTrue(user4 not in changed_task.fields["assignees"].queryset)


class ProjectFormTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username="MainUser", password="Mainpass123"
        )

    def test_create_form_valid_submission(self):
        form_data = {
            "name": "Project",
            "description": "Project for testing",
            "deadline": datetime.today().date(),
            "priority": "high",
            "owner": self.user
        }

        create_form = ProjectCreateForm(data=form_data)

        self.assertTrue(create_form.is_valid())
        create_form.save()

        created_project = Project.objects.last()

        self.assertEqual(created_project.name, form_data["name"])
        self.assertEqual(created_project.description, form_data["description"])

    def test_create_form_invalid_submission(self):
        form_data = {
            "name": "Project",
            "description": "Project for testing",
            "priority": "high",
            "owner": self.user
        }

        create_form = ProjectCreateForm(data=form_data)

        self.assertFalse(create_form.is_valid())

        created_project = Project.objects.last()

        self.assertTrue(created_project is None)


class ValidDeadlineTest(TestCase):
    def test_valid_deadline_future(self):
        future_deadline = datetime.today().date() + timedelta(days=7)
        self.assertEqual(valid_deadline(future_deadline), future_deadline)

    def test_valid_deadline_past(self):
        past_deadline = datetime.today().date() - timedelta(days=7)
        with self.assertRaises(ValidationError) as error:
            valid_deadline(past_deadline)
        self.assertEqual(
            *error.exception,
            "Deadline cannot be in the past!"
        )

    def test_valid_deadline_today_date(self):
        today_deadline = datetime.today().date()
        self.assertEqual(valid_deadline(today_deadline), today_deadline)
