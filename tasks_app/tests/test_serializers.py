from django.test import TestCase
from tasks_app.models import Task, Subtask
from tasks_app.api.serializers import TaskSerializer, SubtaskSerializer
from contacts_app.models import Contact
import datetime


class TaskSerializerTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(name="John Doe", email="john.doe@example.com")
        self.contact.refresh_from_db()

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
        expected_initials = self.contact.first_letters
        expected_profile_pic = self.contact.profile_pic

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
                    "email": "john.doe@example.com",
                    "number": None,
                    "first_letters": expected_initials,
                    "profile_pic": expected_profile_pic,
                }
            ],
            "subtasks": [{"id": str(self.subtask.id), "text": "Test Subtask", "status": "unchecked"}],
        }
        self.assertEqual(serializer.data["id"], expected_data["id"])
        self.assertEqual(serializer.data["title"], expected_data["title"])
        self.assertEqual(len(serializer.data["assigned_to"]), 1)
        serialized_contact = serializer.data["assigned_to"][0]
        self.assertEqual(serialized_contact["id"], expected_data["assigned_to"][0]["id"])
        self.assertEqual(serialized_contact["name"], expected_data["assigned_to"][0]["name"])
        self.assertEqual(serialized_contact["first_letters"], expected_data["assigned_to"][0]["first_letters"])
        self.assertIsNotNone(serialized_contact["profile_pic"])
        self.assertIn("<svg", serialized_contact["profile_pic"])
        self.assertIn(expected_initials, serialized_contact["profile_pic"])
        self.assertEqual(serializer.data["subtasks"], expected_data["subtasks"])

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

    def test_update_existing_subtask(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            category="User Story",
            date=datetime.date.today(),
            prio="medium",
            status="toDo",
        )
        subtask = Subtask.objects.create(task=task, text="Old Subtask", status="unchecked")

        data = {
            "title": "Updated Task",
            "subtasks": [
                {"id": str(subtask.id), "text": "Updated Subtask", "status": "checked"},
            ],
        }
        serializer = TaskSerializer(instance=task, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        subtask.refresh_from_db()
        self.assertEqual(subtask.text, "Updated Subtask")
        self.assertEqual(subtask.status, "checked")

    def test_delete_removed_subtask(self):
        task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            category="User Story",
            date=datetime.date.today(),
            prio="medium",
            status="toDo",
        )
        subtask = Subtask.objects.create(task=task, text="Subtask to Delete", status="unchecked")

        data = {
            "title": "Updated Task",
            "subtasks": [],
        }
        serializer = TaskSerializer(instance=task, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        self.assertFalse(Subtask.objects.filter(id=subtask.id).exists())


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


class TaskSerializerEdgeCaseTest(TestCase):
    def test_validate_task_without_title(self):
        data = {
            "description": "Task without title",
            "category": "Technical Task",
            "date": "2025-04-02",
            "prio": "low",
            "status": "toDo",
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)

    def test_validate_task_with_empty_subtasks(self):
        data = {
            "title": "Task with Empty Subtasks",
            "description": "This task has no subtasks.",
            "category": "Technical Task",
            "date": "2025-04-02",
            "prio": "low",
            "status": "toDo",
            "subtasks": [],
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validate_task_with_invalid_prio(self):
        data = {
            "title": "Invalid Prio Task",
            "description": "This is a test task.",
            "category": "Technical Task",
            "date": "2025-04-02",
            "prio": "invalid",
            "status": "toDo",
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("prio", serializer.errors)

    def test_validate_task_with_invalid_status(self):
        data = {
            "title": "Invalid Status Task",
            "description": "This is a test task.",
            "category": "Technical Task",
            "date": "2025-04-02",
            "prio": "low",
            "status": "invalid",
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)


class SubtaskSerializerEdgeCaseTest(TestCase):
    def test_validate_subtask_without_text(self):
        data = {"text": "", "status": "unchecked"}
        serializer = SubtaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("text", serializer.errors)

    def test_validate_subtask_with_invalid_status(self):
        data = {"text": "Subtask with Invalid Status", "status": "invalid"}
        serializer = SubtaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("status", serializer.errors)


class HandleSubtasksTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            category="User Story",
            date=datetime.date.today(),
            prio="medium",
            status="toDo",
        )

    def test_handle_subtasks_create_and_update(self):
        subtasks_data = [
            {"text": "Subtask 1", "status": "unchecked"},
            {"text": "Subtask 2", "status": "checked"},
        ]
        serializer = TaskSerializer()
        serializer.handle_subtasks(self.task, subtasks_data)
        self.assertEqual(self.task.subtasks.count(), 2)


class TaskSerializerHandleAssignedToTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task.",
            category="User Story",
            date=datetime.date.today(),
            prio="medium",
            status="toDo",
        )

    def test_handle_assigned_to_missing_id(self):
        data = {
            "title": "Updated Task",
            "assigned_to": [{}],
        }
        serializer = TaskSerializer(instance=self.task, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("assigned_to", serializer.errors)
        self.assertEqual(serializer.errors["assigned_to"][0], "Each contact must include an 'id' field.")

    def test_handle_assigned_to_nonexistent_contact(self):
        data = {
            "title": "Updated Task",
            "assigned_to": [{"id": "00000000-0000-0000-0000-000000000000"}],
        }
        serializer = TaskSerializer(instance=self.task, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn("assigned_to", serializer.errors)

        assigned_to_errors = serializer.errors["assigned_to"]
        self.assertIn("id", assigned_to_errors[0])
        self.assertEqual(
            assigned_to_errors[0]["id"][0],
            "Contact with id 00000000-0000-0000-0000-000000000000 does not exist.",
        )
