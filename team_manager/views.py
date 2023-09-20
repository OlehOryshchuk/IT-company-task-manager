from django.shortcuts import render, redirect
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
    TeamJoinLeaveForm,
)


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

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        search_form = WorkerSearchForm(initial={
            "username": username
        })

        context["search_form"] = search_form

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Worker.objects.all().select_related("position")
        username = self.request.GET.get("username", "")
        team_members = self.request.GET.get("team_members", "")

        if username:
            queryset = queryset.filter(username__icontains=username)

        if team_members:
            queryset = queryset.filter(teams=team_members)

        return queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.prefetch_related(
        "tasks", "tasks__owner"
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
        return reverse_lazy(
            "team_manager:worker-detail",
            kwargs={"pk": self.object.pk}
        )


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("team_manager:worker-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    form_class = PositionSearchForm
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name")
        search_form = PositionSearchForm(initial={
            "name": name
        })

        context["search_form"] = search_form

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Position.objects.prefetch_related("workers")
        name = self.request.GET.get("name")

        if name:
            return queryset.filter(name__icontains=name)
        return queryset


class TeamListView(LoginRequiredMixin, generic.ListView):
    model = Team
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        search_form = TeamSearchForm(initial={
            "name": name
        })

        context["search_form"] = search_form

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Team.objects.prefetch_related(
            "members")
        name = self.request.GET.get("name", "")
        worker = self.request.GET.get("members", "")
        project_id = self.request.GET.get("project", "")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if worker:
            queryset = queryset.filter(members=worker)
        if project_id:
            queryset = queryset.filter(projects=project_id)
        return queryset


class TeamDetailView(LoginRequiredMixin, generic.DetailView):
    model = Team
    queryset = Team.objects.prefetch_related(
        "projects", "projects__tasks"
    ).select_related("owner")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["team_join"] = TeamJoinLeaveForm()
        context["team_task"] = Task.objects.filter(project__teams=self.object)

        return context

    def post(self, *args, **kwargs):
        team = self.get_object()

        join_user_to_team = self.request.POST.get("join", "")
        user_left_team = self.request.POST.get("leave", "")

        if join_user_to_team:
            team.members.add(join_user_to_team)

        if user_left_team:
            team.members.remove(user_left_team)

        team.save()

        return redirect("team_manager:team-detail", pk=team.pk)


class TeamCreateView(LoginRequiredMixin, generic.CreateView):
    model = Team
    form_class = TeamCreationForm
    success_url = reverse_lazy("team_manager:team-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Team
    form_class = TeamCreationForm

    def get_success_url(self):
        return reverse_lazy(
            "team_manager:team-detail",
            kwargs={"pk": self.object.pk}
        )

    def post(self, request, *args, **kwargs):
        team = self.get_object()

        selected_projects = request.POST.getlist("projects")

        team.projects.set(selected_projects)

        return super().post(request, *args, **kwargs)


class TeamDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Team
    success_url = reverse_lazy("team_manager:team-list")
