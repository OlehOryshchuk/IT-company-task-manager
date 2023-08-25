from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import datetime

from .models import Task, Project, TaskType
from team_manager.models import Team


class TaskFilterForm(forms.ModelForm):
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        empty_label="Filter by task type",
        required=False,
    )
    is_completed = forms.ChoiceField(
        choices=(
            (False, "Not completed"),
            (True, "Completed")
        ),
        required=False,
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Task
        fields = ["task_type", "tags", "is_completed"]


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search by task's name"
        }
        )
    )


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search by project's name"
        }
        )
    )


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "owner": forms.HiddenInput(),
            "is_completed": forms.HiddenInput(),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        return valid_deadline(deadline)


class TaskChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "assignees",
            "is_completed",
        )


class ProjectCreateForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "owner": forms.HiddenInput(),
            "is_completed": forms.HiddenInput(),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        return valid_deadline(deadline)


def valid_deadline(deadline: datetime) -> datetime:
    if deadline < datetime.today().date():
        raise ValidationError("Deadline cannot be in the past!")

    return deadline
