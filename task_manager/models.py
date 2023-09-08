from django.db import models
from IT_company_task_manager.settings import AUTH_USER_MODEL
from taggit_autosuggest.managers import TaggableManager

from team_manager.models import Team


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


PRIORITY_CHOICES = [
    ("urgent", "Urgent"),
    ("high", "High"),
    ("medium", "Medium"),
    ("low", "Low"),
]


class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(
        help_text="Enter the deadline for this task.",
    )
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        default="medium",
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        AUTH_USER_MODEL,
        related_name="tasks",
    )
    tags = TaggableManager(
        related_name="tasks",
        blank=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="my_tasks",
        on_delete=models.CASCADE,
        null=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "task"
        verbose_name_plural = "tasks"

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=50,
        choices=PRIORITY_CHOICES,
        default="medium",
    )
    deadline = models.DateField(
        help_text="Enter the deadline for this task.",
    )
    teams = models.ManyToManyField(
        Team,
        related_name="projects",
    )
    tags = TaggableManager(
        related_name="projects",
        blank=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name="projects",
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["name"]

    def __str__(self):
        return self.name
