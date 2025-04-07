from django.db import models
import uuid


class Contact(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(primary_key=True, unique=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    first_letters = models.CharField(max_length=2, blank=True, null=True)
    is_user = models.BooleanField(default=False)
    profile_pic = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
