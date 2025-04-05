from rest_framework.test import APITestCase
from rest_framework import status
from tasks_app.models import Task, Subtask
from contacts_app.models import Contact
import datetime
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class TaskViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

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
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

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


class SummaryViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

        self.contact = Contact.objects.create(name="John Doe", mail="john.doe@example.com")

        Task.objects.create(
            title="Task 1",
            description="To Do Task",
            category="User Story",
            date=datetime.date.today(),
            prio="medium",
            status="toDo",
        )

        Task.objects.create(
            title="Task 2",
            description="In Progress Task",
            category="Technical Task",
            date=datetime.date.today(),
            prio="urgent",
            status="inProgress",
        )

        Task.objects.create(
            title="Task 3",
            description="Await Feedback Task",
            category="User Story",
            date=datetime.date.today(),
            prio="low",
            status="awaitFeedback",
        )

        Task.objects.create(
            title="Task 4",
            description="Done Task",
            category="Technical Task",
            date=datetime.date.today(),
            prio="urgent",
            status="done",
        )

    def test_summary_view(self):
        response = self.client.get("/api/tasks/summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            "todos": 1,
            "in_progress": 1,
            "await_feedback": 1,
            "done": 1,
            "total": 4,
            "urgent": 2,
        }
        self.assertEqual(response.data, expected_data)

    def test_summary_view_no_tasks(self):
        Task.objects.all().delete()
        response = self.client.get("/api/tasks/summary/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "No tasks found"})

    def test_summary_view_method_not_allowed(self):
        response = self.client.post("/api/tasks/summary/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response.data, {"detail": 'Method "POST" not allowed.'})
