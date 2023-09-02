from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date, datetime

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
            "placeholder": "Search by task name",
        }
        )
    )


class ProjectSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search by project name",
        }
        )
    )


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
        queryset=None,
    )

    class Meta:
        model = Task
        fields = "__all__"
        widgets = {
            "owner": forms.HiddenInput(),
            "is_completed": forms.HiddenInput(),
            "deadline": forms.DateInput(attrs={
                "type": "date",
                })
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assignees"].queryset = get_user_model().objects.filter(
            teams__members=user
        )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        return valid_deadline(deadline)


class TaskChangeStatusForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
        queryset=None
    )
    is_completed = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
    )

    class Meta:
        model = Task
        fields = (
            "assignees",
            "is_completed",
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["assignees"].queryset = get_user_model().objects.filter(
            teams__members=user
        )

    def save(self, commit=True):
        task = super().save(commit=False)

        update_assignees = self.cleaned_data.get("assignees", [])
        update_is_completed = self.cleaned_data.get("is_completed", "")

        task.assignees.clear()
        task.assignees.add(*update_assignees)

        if update_is_completed:
            task.is_completed = True
        else:
            task.is_completed = False

        if commit:
            task.save()

        return task


class ProjectCreateForm(forms.ModelForm):
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Project
        fields = "__all__"
        widgets = {
            "owner": forms.HiddenInput(),
            "is_completed": forms.HiddenInput(),
            "deadline": forms.DateInput(attrs={
                "type": "date",
            })
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")
        return valid_deadline(deadline)


def valid_deadline(deadline: date) -> date:
    if deadline < datetime.today().date():
        raise ValidationError("Deadline cannot be in the past!")

    return deadline
