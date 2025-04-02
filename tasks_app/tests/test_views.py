from rest_framework.test import APITestCase
from rest_framework import status
from tasks_app.models import Task
from contacts_app.models import Contact
import datetime


class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="John Doe", mail="john.doe@example.com")
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            category="User Story",
            date=datetime.date.today(),
            prio="medium",
            status="toDo",
        )
        self.task.assigned_to.add(self.contact)

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "This is a new task.",
            "category": "Technical Task",
            "date": "2025-04-02",
            "prio": "urgent",
            "status": "inProgress",
            "assigned_to": [{"id": str(self.contact.id)}],
            "subtasks": [{"text": "New Subtask", "status": "unchecked"}],
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")
