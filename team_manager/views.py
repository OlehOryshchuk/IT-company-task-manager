from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import QuerySet

from .models import Worker, Position, Team
from task_manager.models import Task, Project

from .form import (
    WorkerSearchForm,
    WorkerCreationForm,
    PositionSearchForm,
    TeamCreationForm,
    TeamSearchForm,
)


@login_required
def index(request):
    num_completed_projects = Project.objects.filter(is_completed=True).count()
    num_completed_tasks = Task.objects.filter(is_completed=True).count()
    num_teams = Team.objects.count()
    num_workers = Worker.objects.count()

    context = {
        "num_completed_projects": num_completed_projects,
        "num_completed_tasks": num_completed_tasks,
        "num_teams": num_teams,
        "num_workers": num_workers,
    }

    return render(request, "index.html", context=context)

