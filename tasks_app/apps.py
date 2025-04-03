from django.apps import AppConfig


class TasksAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks_app"
    verbose_name = "Tasks Management"
    verbose_name_plural = "Tasks Management"
