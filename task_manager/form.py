from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from datetime import datetime
from taggit_autosuggest.widgets import TagAutoSuggest
from taggit.models import Tag

from .models import Task


class TagSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search task by tag"
        }
        )

    )


class TaskTypeSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        label="",
        required=False,
        widget=forms.TextInput(attrs={
            "placeholder": "Search task by type name"
        }
        )

    )


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


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=TagAutoSuggest(
            attrs={
                "data_autocomplete_url": reverse_lazy("taggit_autosuggest-list")
            },
            tagmodel=Tag),
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

        if deadline < datetime.today().date():
            raise ValidationError("Deadline cannot be in the past!")

        return deadline


class TaskChangeStatusForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "assignees",
            "is_completed",
        )
        widgets = {
            "assignees": forms.HiddenInput(),
            "is_completed": forms.HiddenInput(),
        }

