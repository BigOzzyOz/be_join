"""
App configuration for the contacts_app Django application.
"""

from django.apps import AppConfig


class ContactsAppConfig(AppConfig):
    """
    Configuration for the Contacts Management app, including verbose names and signal registration.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "contacts_app"
    verbose_name = "Contacts Management"
    verbose_name_plural = "Contacts Management"

    def ready(self):
        """
        Import signals to ensure they are registered when the app is ready.
        """
        import contacts_app.signals
