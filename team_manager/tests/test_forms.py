from django.test import TestCase

from ..form import (
    PositionSearchForm,

    WorkerCreationForm,
    WorkerSearchForm,

    TeamSearchForm,
    TeamCreationForm,
    TeamJoinRemoveForm,
)


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
