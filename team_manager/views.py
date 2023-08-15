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


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        search_form = WorkerSearchForm(initial={
            "username": username
        })

        context["search_form"] = search_form

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.all().select_related("position")
        username = self.request.GET.get("username")

        if username:
            return queryset.filter(username__icontains=username)
        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related(
        "tasks__task_type", "tasks__tags", 'teams'
    )


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("team_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "position",
    ]

    def get_success_url(self):
        return reverse_lazy("team_manager:worker-detail", kwargs={"pk": self.object.pk})


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("team_manager:worker-list")



