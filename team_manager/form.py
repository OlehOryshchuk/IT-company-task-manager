from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Worker, Team


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by position's name"
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
                "placeholder": "Search by worker's username",
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
    class Meta:
        model = Team
        fields = "__all__"
        widgets = {
            "owner": forms.HiddenInput()
        }
