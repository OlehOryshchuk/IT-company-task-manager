from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from datetime import datetime

from ..models import TaskType, Task, Project


TASK_TYPE_CREATE = reverse_lazy("task_manager:task-type-create")

TASK_LIST = reverse_lazy("task_manager:task-list")
TASK_CREATE = reverse_lazy("task_manager:task-create")

PROJECT_LIST = reverse_lazy("task_manager:project-list")
PROJECT_CREATE = reverse_lazy("task_manager:project-create")

