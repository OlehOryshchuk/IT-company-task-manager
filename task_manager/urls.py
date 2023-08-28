from django.urls import path
from .views import (
    TaskTypeCreateView,

    task_filter_view,
    TaskListView,
    TaskCreateView,
    TaskDeleteView,
    TaskUpdateView,
    TaskDetailView,

    ProjectListView,
    ProjectDeleteView,
    ProjectCreateView,
    ProjectUpdateView,
    ProjectDetailView,

)

urlpatterns = [
    path(
        "task_type/create/",
        TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "task/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "task/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "task/<int:pk>/delete",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "task/<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "task/filter/",
        task_filter_view,
        name="task-filter",
    ),
    path(
        "projects/",
        ProjectListView.as_view(),
        name="project-list"
    ),
    path(
        "project/create/",
        ProjectCreateView.as_view(),
        name="project-create"
    ),
    path(
        "project/<int:pk>/update/",
        ProjectUpdateView.as_view(),
        name="project-update"
    ),
    path(
        "project/<int:pk>/delete",
        ProjectDeleteView.as_view(),
        name="project-delete"
    ),
    path(
        "project/<int:pk>/detail",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
    path(
        "projects/",
        ProjectListView.as_view(),
        name="project-list"
    ),
]

app_name = "task_manager"
