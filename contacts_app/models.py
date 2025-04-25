"""
Models for storing contact information, including user linkage and profile visuals.
"""

from django.db import models
from django.contrib.auth.models import User
import uuid


class Contact(models.Model):
    """
    Represents a contact with name, email, number, initials, profile picture, and optional user linkage.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=30, blank=True, null=True)
    first_letters = models.CharField(max_length=2, blank=True, null=True)
    is_user = models.BooleanField(default=False)
    profile_pic = models.TextField(blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="contact")

    def __str__(self):
        """Return the contact's name as string representation."""
        return self.name
