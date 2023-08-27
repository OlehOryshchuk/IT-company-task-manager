from django.test import TestCase
from django.contrib.auth import get_user_model

from ..form import (
    TaskFilterForm,
    TaskSearchForm,
    TaskCreateForm,
    TaskChangeStatusForm,

    ProjectSearchForm,
    ProjectCreateForm,

    valid_deadline
)
from ..models import TaskType


class TaskFormTest(TestCase):
    def setUp(self) -> None:
        self.filter_form = TaskFilterForm()
        self.user = get_user_model().objects.create(
            username="testuser", password="test123"
        )

    def test_filter_form_empty_label_and_required_should_be_false(self):
        self.assertEqual(self.filter_form.fields["task_type"].empty_label, "Filter by task type")
        self.assertTrue(self.filter_form.fields["task_type"].required is False)
        self.assertTrue(self.filter_form.fields["is_completed"].required is False)

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

    def test_form_valid_data(self):
        task_type = TaskType.objects.create(name="bug")
        form_data = {
            "name": "Test Task",
            "description": "This is a test task",
            "deadline": "2023-08-31",
            "priority": "high",
            "task_type": task_type.id,
            "owner": self.user.id,
            "is_completed": True,
        }

        form = TaskCreateForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_form_invalid_data(self):
        form_data = {
            "name": "Test Task",
            "priority": "high",
        }

        form = TaskCreateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
