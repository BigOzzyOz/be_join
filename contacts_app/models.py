from django.db import models
import uuid


class Contact(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    mail = models.EmailField(unique=True)
    number = models.CharField(max_length=20, blank=True, null=True)
    first_letters = models.CharField(max_length=2, blank=True, null=True)
    profile_pic = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
