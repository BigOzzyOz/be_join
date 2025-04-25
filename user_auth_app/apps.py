"""
App configuration for the user_auth_app Django application.
"""

from django.apps import AppConfig


class UserAuthAppConfig(AppConfig):
    """
    Configuration for the Authentication app, including verbose names and signal registration.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "user_auth_app"
    verbose_name = "Authentication"
    verbose_name_plural = "Authentications"

    def ready(self):
        """
        Import signals to ensure they are registered when the app is ready.
        """
        import user_auth_app.signals
