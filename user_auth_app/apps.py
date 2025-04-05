from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "user_auth_app"
    verbose_name = "Authentication"
    verbose_name_plural = "Authentications"

    def ready(self):
        import user_auth_app.signals
