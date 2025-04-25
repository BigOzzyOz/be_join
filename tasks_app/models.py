"""
Models for storing tasks and subtasks, including priorities, categories, and assignments.
"""

from django.db import models
import uuid
from contacts_app.models import Contact


class Task(models.Model):
    """
    Represents a task with title, description, category, date, priority, status, and assigned contacts.
    """

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("toDo", "To Do"),
        ("inProgress", "In Progress"),
        ("awaitFeedback", "Await Feedback"),
        ("done", "Done"),
    ]

    CATEGORY_CHOICES = [("User Story", "User Story"), ("Technical Task", "Technical Task")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    date = models.DateField()
    prio = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="toDo")
    assigned_to = models.ManyToManyField(Contact, related_name="tasks", blank=True)

    def __str__(self):
        """Return the task's title as string representation."""
        return self.title

    class Meta:
        ordering = ["-date"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Subtask(models.Model):
    """
    Represents a subtask belonging to a task, with text and status.
    """

    STATUS_CHOICES = [
        ("checked", "Checked"),
        ("unchecked", "Unchecked"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="unchecked")

    def __str__(self):
        """Return the subtask's text as string representation."""
        return self.text

    class Meta:
        ordering = ["id"]
        verbose_name = "Subtask"
        verbose_name_plural = "Subtasks"
