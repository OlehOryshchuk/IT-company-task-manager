from django.db import models
from it_company_task_manager.settings import AUTH_USER_MODEL
from taggit_autosuggest.managers import TaggableManager


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
        blank=True,
    )
    tags = TaggableManager(
        related_name="tasks",
        blank=True,
    )
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="tasks"
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

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"
        ordering = ["name"]

    def __str__(self):
        return self.name
