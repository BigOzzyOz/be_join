from django.contrib import admin
from tasks_app.models import Task, Subtask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "date", "prio", "status")
    search_fields = ("title", "description")
    list_filter = ("category", "prio", "status", "date")
    filter_horizontal = ("assigned_to",)


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ("text", "task", "status")
    search_fields = ("text",)
    list_filter = ("status",)
