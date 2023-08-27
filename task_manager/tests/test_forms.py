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

    def test_filter_form_empty_label_and_required_should_be_false(self):
        self.assertEqual(self.filter_form.fields["task_type"].empty_label, "Filter by task type")
        self.assertTrue(self.filter_form.fields["task_type"].required is False)
        self.assertTrue(self.filter_form.fields["is_completed"].required is False)


