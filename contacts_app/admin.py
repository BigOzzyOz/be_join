from django.contrib import admin
from contacts_app.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "mail", "number", "first_letters")
    search_fields = ("name", "mail")
    list_filter = ("first_letters",)
