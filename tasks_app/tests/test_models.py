from django.test import TestCase
from tasks_app.models import Task, Subtask
from contacts_app.models import Contact
import datetime
from django.utils import timezone


class TaskModelTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="John Doe", email="john.doe@example.com")
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
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.category, "User Story")
        self.assertEqual(self.task.prio, "medium")
        self.assertEqual(self.task.status, "toDo")
        self.assertIn(self.contact, self.task.assigned_to.all())

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), "Test Task")


class SubtaskModelTest(TestCase):
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

    def test_create_subtask(self):
        self.assertEqual(self.subtask.text, "Test Subtask")
        self.assertEqual(self.subtask.status, "unchecked")
        self.assertEqual(self.subtask.task, self.task)

    def test_subtask_string_representation(self):
        self.assertEqual(str(self.subtask), "Test Subtask")


class TaskModelEdgeCaseTest(TestCase):
    def test_create_task_without_description(self):
        task = Task.objects.create(
            title="Task Without Description",
            category="User Story",
            date=timezone.now().date(),
            prio="low",
            status="toDo",
        )
        self.assertIsNotNone(task.pk)
        self.assertEqual(task.title, "Task Without Description")
        self.assertIsNone(task.description)
