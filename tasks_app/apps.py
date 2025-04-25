"""
App configuration for the tasks_app Django application.
"""

from django.apps import AppConfig


class TasksAppConfig(AppConfig):
    """
    Configuration for the Tasks Management app, including verbose names.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks_app"
    verbose_name = "Tasks Management"
    verbose_name_plural = "Tasks Management"
