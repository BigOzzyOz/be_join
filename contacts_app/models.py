from django.db import models
from django.contrib.auth.models import User
import uuid


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    first_letters = models.CharField(max_length=2, blank=True, null=True)
    is_user = models.BooleanField(default=False)
    profile_pic = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="contact")

    def __str__(self):
        return self.name
