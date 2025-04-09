from django.contrib import admin
from contacts_app.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "first_letters", "user")
    search_fields = ("name", "email", "user")
    list_filter = ("first_letters",)
    ordering = ("name",)
