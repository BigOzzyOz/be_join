from django.db import models
import uuid
from contacts_app.models import Contact


class Task(models.Model):
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
    description = models.TextField()
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    date = models.DateField()
    prio = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="low")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="toDo")
    assigned_to = models.ManyToManyField(Contact, related_name="tasks")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-date"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Subtask(models.Model):
    STATUS_CHOICES = [
        ("checked", "Checked"),
        ("unchecked", "Unchecked"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE)
    text = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="unchecked")

    def __str__(self):
        return self.text

    class Meta:
        ordering = ["id"]
        verbose_name = "Subtask"
        verbose_name_plural = "Subtasks"
