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


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    context_object_name = "task_type"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task_manager:task-list")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        search_form = TaskSearchForm(initial={
            "name": name
        })

        context["search_form"] = search_form

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related(
            "assignees", "tags"
        )

        name = self.request.GET.get("name", "")
        task_type = self.request.GET.get("task_type", "")
        tags = self.request.GET.get("tags", "").strip(",")  # remove coma ',' that taggit_auttosugest is adding to tags
        is_completed = self.request.GET.get("is_completed", "")

        self.request.session["task_filter"] = {
            "task_type": task_type,
            "tags": tags,
            "is_completed": is_completed,
        }

        if name:
            queryset = queryset.filter(name__icontains=name)

        if task_type:
            queryset = queryset.filter(task_type=task_type)

        if tags:
            queryset = queryset.filter(tags__name__in=tags.split(","))  # convert string to list of tags

        if is_completed == "True":
            queryset = queryset.filter(is_completed=True)

        if is_completed == "False":
            queryset = queryset.filter(is_completed=False)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.prefetch_related(
        "assignees", "tags"
    ).select_related(
        "project"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_form"] = TaskChangeStatusForm(instance=self.object, user=self.request.user)

        for user_team in self.request.user.teams.all():
            if user_team in self.object.project.teams.all():
                context["valid_user"] = True
                break

        context["is_past_deadline"] = valid_deadline(deadline=self.object.deadline)

        return context

    def post(self, *args, **kwargs):
        task = self.get_object()

        update_task = TaskChangeStatusForm(user=self.request.user, instance=task, data=self.request.POST)

        if update_task.is_valid():
            update_task.save()

        return redirect("task_manager:task-detail", pk=task.id)


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm

    def get_success_url(self):
        return reverse_lazy("task_manager:task-detail", kwargs={"pk": self.object.id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateForm

    def get_success_url(self):
        return reverse_lazy("task_manager:task-detail", kwargs={"pk": self.object.pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")


class ProjectListView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")

        search_form = ProjectSearchForm(initial={"name": name})

        context["search_form"] = search_form

        return context

    def get_queryset(self) -> QuerySet:
        queryset = Project.objects.prefetch_related(
            "teams", "tasks"
        )
        name = self.request.GET.get("name", "")
        team_projects = self.request.GET.get("team_projects", "")

        if name:
            queryset = queryset.filter(name__icontains=name)

        if team_projects:
            queryset = queryset.filter(teams=team_projects)

        return queryset


class ProjectDetailView(LoginRequiredMixin, generic.DetailView):
    model = Project
    queryset = Project.objects.prefetch_related(
        "teams", "tags"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["is_past_deadline"] = valid_deadline(deadline=self.object.deadline)

        return context


class ProjectCreateView(LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectCreateForm

    def get_success_url(self):
        return reverse_lazy("task_manager:project-detail", kwargs={"pk": self.object.id})


class ProjectUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Project
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy("task_manager:project-detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Project
    success_url = reverse_lazy("task_manager:project-list")
