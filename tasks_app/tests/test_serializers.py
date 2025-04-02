from django.test import TestCase
from tasks_app.models import Task, Subtask
from tasks_app.api.serializers import TaskSerializer, SubtaskSerializer
from contacts_app.models import Contact
import datetime


class TaskSerializerTest(TestCase):
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
        self.subtask = Subtask.objects.create(task=self.task, text="Test Subtask", status="unchecked")

    def test_serialize_task(self):
        serializer = TaskSerializer(self.task)
        print(serializer.data)  # Debugging-Ausgabe
        expected_data = {
            "id": str(self.task.id),
            "title": "Test Task",
            "description": "This is a test task.",
            "category": "User Story",
            "date": str(self.task.date),
            "prio": "medium",
            "prio_display": "Medium",
            "status": "toDo",
            "status_display": "To Do",
            "assigned_to": [
                {
                    "id": str(self.contact.id),
                    "name": "John Doe",
                    "mail": "john.doe@example.com",
                    "number": None,
                    "first_letters": None,
                    "profile_pic": None,
                }
            ],
            "subtasks": [{"id": str(self.subtask.id), "text": "Test Subtask", "status": "unchecked"}],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_validate_task_with_invalid_data(self):
        data = {
            "title": "",
            "description": "This is a test task.",
            "category": "Invalid Category",
            "date": "2025-04-02",
            "prio": "invalid",
            "status": "invalid",
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
        self.assertIn("category", serializer.errors)
        self.assertIn("prio", serializer.errors)
        self.assertIn("status", serializer.errors)


class SubtaskSerializerTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            category="User Story",
            date=datetime.date.today(),
            prio="medium",
            status="toDo",
        )
        self.subtask = Subtask.objects.create(task=self.task, text="Test Subtask", status="unchecked")

    def test_serialize_subtask(self):
        serializer = SubtaskSerializer(self.subtask)
        expected_data = {
            "id": str(self.subtask.id),
            "text": "Test Subtask",
            "status": "unchecked",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_validate_subtask_with_invalid_data(self):
        data = {"text": "", "status": "invalid"}
        serializer = SubtaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("text", serializer.errors)
        self.assertIn("status", serializer.errors)
