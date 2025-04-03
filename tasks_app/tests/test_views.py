from rest_framework.test import APITestCase
from rest_framework import status
from tasks_app.models import Task, Subtask
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


class TaskViewSetEdgeCaseTest(APITestCase):
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

    def test_create_task_without_assigned_to(self):
        data = {
            "title": "Task Without Assigned To",
            "description": "This task has no assigned contacts.",
            "category": "Technical Task",
            "date": "2025-04-02",
            "prio": "low",
            "status": "toDo",
            "assigned_to": [],
            "subtasks": [{"text": "Subtask", "status": "unchecked"}],
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Task Without Assigned To")

    def test_update_task_with_invalid_data(self):
        data = {
            "title": "",
            "description": "Updated description",
            "category": "Invalid Category",
            "prio": "invalid",
            "status": "invalid",
        }
        response = self.client.put(f"/api/tasks/{self.task.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertIn("category", response.data)

    def test_delete_task_with_subtasks(self):
        subtask = Subtask.objects.create(task=self.task, text="Subtask to Delete", status="unchecked")
        response = self.client.delete(f"/api/tasks/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
        self.assertFalse(Subtask.objects.filter(id=subtask.id).exists())
