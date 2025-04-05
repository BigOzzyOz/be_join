from django.contrib import admin
from user_auth_app.models import ProfileUser


@admin.register(ProfileUser)
class ProfileUserAdmin(admin.ModelAdmin):
    list_display = ("user__username", "user__email", "id")
    search_fields = ("user__username", "user__email")
    list_filter = ("user__is_active", "user__is_staff")
    ordering = ("user__username",)
