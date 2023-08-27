from django.contrib import admin

from .models import TaskType, Task, Project


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_filter = ["tags__tasks"]
    list_display = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority"
    ]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "deadline",
        "is_completed",
        "priority"
    ]
    search_fields = ["name"]
    list_filter = ["name"]
