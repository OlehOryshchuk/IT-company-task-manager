from django.urls import path

from .views import (
    index,
    WorkerListView,
    WorkerDetailView,
    WorkerCreateView,
    WorkerUpdateView,
    WorkerDeleteView,

    PositionListView,

    TeamListView,
    TeamDetailView,
    TeamCreateView,
    TeamUpdateView,
    TeamDeleteView
)

urlpatterns = [
    path("", index, name="index"),
    path(
        "workers/",
        WorkerListView.as_view(),
        name="worker-list",
    ),
    path(
        "worker/<int:pk>/",
        WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "worker/create/",
        WorkerCreateView.as_view(),
        name="worker-create"
    ),
    path(
        "worker/<int:pk>/update/",
        WorkerUpdateView.as_view(),
        name="worker-update"
    ),
    path(
        "worker/<int:pk>/delete/",
        WorkerDeleteView.as_view(),
        name="worker-delete"
    ),
    path(
        "positions/",
        PositionListView.as_view(),
        name="position-list",
    ),
    path(
        "teams/",
        TeamListView.as_view(),
        name="team-list",
    ),
    path(
        "team/<int:pk>/",
        TeamDetailView.as_view(),
        name="team-detail"
    ),
    path(
        "team/create/",
        TeamCreateView.as_view(),
        name="team-create"
    ),
    path(
        "team/<int:pk>/update/",
        TeamUpdateView.as_view(),
        name="team-update"
    ),
    path(
        "team/<int:pk>/delete/",
        TeamDeleteView.as_view(),
        name="team-delete"
    ),

]

app_name = "team_manager"
