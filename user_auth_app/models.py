from django.db import models
from django.contrib.auth.models import User
import uuid


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile User"
        verbose_name_plural = "Profile Users"
        ordering = ["user__username"]
