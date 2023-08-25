import datetime
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import QuerySet

from .models import TaskType, Task, Project
from .form import (
    TaskFilterForm,
    TaskSearchForm,
    TaskCreateForm,
    TaskChangeStatusForm,
    ProjectSearchForm,
    ProjectCreateForm,
)


def valid_deadline(deadline: datetime) -> bool:
    if deadline < datetime.date.today():
        return True
    return False


def task_filter_view(request):
    if request.GET.get("reset"):
        request.session.pop("task_filter", None)  # Remove the session filter data

    context = {
        "task_filter": TaskFilterForm(initial=request.session.get("task_filter", {}))
    }

    return render(request, "task_manager/task_filter.html", context=context)
