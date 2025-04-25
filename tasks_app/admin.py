"""
Admin configuration for the Task and Subtask models in the Django admin interface.
"""

from django.contrib import admin
from tasks_app.models import Task, Subtask


class SubtaskInline(admin.TabularInline):
    """
    Inline admin for editing Subtasks within a Task in the admin interface.
    """

    model = Subtask
    fields = ("text", "status")
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface options for Task: list display, search, filter, ordering, and subtasks inline.
    """

    list_display = ("title", "category", "date", "prio", "status")
    search_fields = ("title", "description")
    list_filter = ("category", "prio", "status", "date")
    filter_horizontal = ("assigned_to",)
    ordering = ("-date",)
    inlines = [SubtaskInline]


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    """
    Admin interface options for Subtask: list display, search, filter, and ordering.
    """

    list_display = ("text", "task", "status")
    search_fields = ("text",)
    list_filter = ("status",)
    ordering = ("-task__date",)
