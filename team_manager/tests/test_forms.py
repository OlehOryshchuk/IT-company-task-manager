from django.test import TestCase
from django.contrib.auth import get_user_model

from ..form import (
    PositionSearchForm,

    WorkerCreationForm,
    WorkerSearchForm,

    TeamSearchForm,
    TeamCreationForm,
    TeamJoinRemoveForm,
)
from ..models import Position


class PositionFormTest(TestCase):

    def setUp(self) -> None:
        self.form = PositionSearchForm()

    def test_search_form_field_and_label(self):
        self.assertTrue(self.form.fields.get("name"))
        self.assertTrue(self.form.fields["name"].label == "")

    def test_search_form_placeholder(self):
        rendered_html = self.form.as_p()

        self.assertIn('placeholder="Search by position name"', rendered_html)

    def test_search_form_is_not_required(self):
        self.assertFalse(self.form.fields["name"].required)


class WorkerFormTest(TestCase):

    def setUp(self) -> None:
        self.search_form = WorkerSearchForm()

    def test_search_form_field_and_label(self):
        self.assertTrue(self.search_form.fields.get("username"))
        self.assertTrue(self.search_form.fields["username"].label == "")

    def test_search_form_placeholder(self):
        rendered_html = self.search_form.as_p()

        self.assertIn('placeholder="Search by worker username"', rendered_html)

    def test_search_form_is_not_required(self):
        self.assertFalse(self.search_form.fields["username"].required)

    def test_creation_form_fields(self):
        create_form = WorkerCreationForm()

        expected_fields = ["username", "position", "first_name", "last_name", "password1", "password2"]

        self.assertEqual(list(create_form.fields.keys()), expected_fields)

    def test_create_form_submission(self):
        creation_form_data = {
            "username": "testusername",
            "position": Position.objects.create(name="developer").id,
            "first_name": "test_name",
            "last_name": "test_last_name",
            "password1": "test_password123",
            "password2": "test_password123",
        }

        valid_worker = WorkerCreationForm(data=creation_form_data)
        self.assertTrue(valid_worker.is_valid())


class TeamFormTest(TestCase):

    def setUp(self) -> None:
        self.search_form = TeamSearchForm()

        self.worker = get_user_model().objects.create_user(
            username="username1",
            position=Position.objects.create(name="QA"),
            password="worker_password",
        )

    def test_search_form_field_and_label(self):
        self.assertTrue(self.search_form.fields.get("name"))
        self.assertTrue(self.search_form.fields["name"].label == "")

    def test_search_form_placeholder(self):
        rendered_html = self.search_form.as_p()

        self.assertIn('placeholder="Search by project name"', rendered_html)

    def test_search_form_is_not_required(self):
        self.assertFalse(self.search_form.fields["name"].required)

    def test_creation_form_fields(self):
        create_form = TeamCreationForm()

        expected_fields = ["name", "description", "members", "owner", "projects"]

        self.assertEqual(list(create_form.fields.keys()), expected_fields)

    def test_create_form_valid_submission(self):
        creation_form_data = {
           "name": "testname",
           "owner": self.worker,
        }

        valid_team = TeamCreationForm(data=creation_form_data)
        self.assertTrue(valid_team.is_valid())

    def test_create_form_invalid_submission(self):
        creation_form_data = {
           "name": "",
           "owner": self.worker,
        }

        valid_team = TeamCreationForm(data=creation_form_data)
        self.assertFalse(valid_team.is_valid())

    def test_join_leave_form_field(self):
        join_leave_team = TeamJoinRemoveForm()

        self.assertTrue(join_leave_team.fields.get("members"))
