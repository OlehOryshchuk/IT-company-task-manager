from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse_lazy, reverse

from ..models import Position, Team

POSITION_LIST = reverse_lazy("team_manager:position-list")

WORKER_LIST = reverse_lazy("team_manager:worker-list")
CREATE_WORKER = reverse_lazy("team_manager:worker-create")

TEAM_LIST = reverse_lazy("team_manager:team-list")
CREATE_TEAM = reverse_lazy("team_manager:team-create")
