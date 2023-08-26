from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Worker, Team
from task_manager.models import Project


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by position name"
            }
        )
    )


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by worker username",
                "size": 30,
            }
        )
    )


class TeamSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by project name",
                "size": 30,
            }
        )
    )


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + (
            "position",
            "first_name",
            "last_name",
        )


class TeamCreationForm(forms.ModelForm):
    projects = forms.ModelMultipleChoiceField(
        queryset=Project.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )
    members = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple()
    )

    class Meta:
        model = Team
        fields = "__all__"
        widgets = {
            "owner": forms.HiddenInput()
        }


class TeamJoinLeaveForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["members"]
        widgets = {
            "members": forms.HiddenInput()
        }

