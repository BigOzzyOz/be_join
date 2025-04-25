# -*- coding: utf-8 -*-
import datetime
from contacts_app.models import Contact
from tasks_app.models import Task, Subtask

# --- Kontakte anlegen ---
contacts_data = [
    {"name": "Alice Anderson", "email": "alice.anderson@webmail.de", "number": "+4915112345678"},
    {"name": "Bob Baker", "email": "bob.baker@company.com", "number": "+4915223456789"},
    {"name": "Carla Schmidt", "email": "carla.schmidt@uni-hamburg.de", "number": "+4915334567890"},
    {"name": "David Müller", "email": "d.mueller@it-consulting.de", "number": "+4915445678901"},
    {"name": "Eva Klein", "email": "eva.klein@posteo.net", "number": "+4915556789012"},
    {"name": "Frank Nowak", "email": "frank.nowak@freemail.de", "number": "+4915667890123"},
    {"name": "Gina Hoffmann", "email": "gina.hoffmann@startup.io", "number": "+4915778901234"},
    {"name": "Hannes Weber", "email": "hannes.weber@devmail.com", "number": "+4915889012345"},
    {"name": "Ines Fischer", "email": "ines.fischer@schule.de", "number": "+4915990123456"},
    {"name": "Jonas Krüger", "email": "jonas.krueger@projektmail.de", "number": "+4916012345678"},
]
contacts = []
for c in contacts_data:
    contact, created = Contact.objects.get_or_create(
        email=c["email"],
        defaults={
            "name": c["name"],
            "number": c["number"],
        },
    )
    contacts.append(contact)

# --- Tasks anlegen ---
task_templates = [
    {
        "title": "Set up Django project structure",
        "category": "Technical Task",
        "prio": "urgent",
        "status": "done",
        "description": "Initialize the Django project and apps for backend development.",
        "subtasks": [
            {"text": "Create virtual environment", "status": "checked"},
            {"text": "Install Django", "status": "checked"},
            {"text": "Start project and apps", "status": "checked"},
        ],
        "assigned": [0, 1],
        "date": datetime.date.today() - datetime.timedelta(days=14),
    },
    {
        "title": "Design REST API endpoints",
        "category": "User Story",
        "prio": "medium",
        "status": "inProgress",
        "description": "Define endpoints for tasks, contacts, and authentication.",
        "subtasks": [
            {"text": "List all endpoints", "status": "checked"},
            {"text": "Document API structure", "status": "unchecked"},
        ],
        "assigned": [2, 3],
        "date": datetime.date.today() - datetime.timedelta(days=10),
    },
    {
        "title": "Implement authentication",
        "category": "Technical Task",
        "prio": "urgent",
        "status": "toDo",
        "description": "Add user registration, login, and token authentication.",
        "subtasks": [
            {"text": "User registration", "status": "unchecked"},
            {"text": "Token login", "status": "unchecked"},
        ],
        "assigned": [4],
        "date": datetime.date.today() - datetime.timedelta(days=7),
    },
    {
        "title": "Create models for tasks and contacts",
        "category": "Technical Task",
        "prio": "medium",
        "status": "done",
        "description": "Define Django models for tasks, subtasks, and contacts.",
        "subtasks": [
            {"text": "Task model", "status": "checked"},
            {"text": "Subtask model", "status": "checked"},
            {"text": "Contact model", "status": "checked"},
        ],
        "assigned": [5, 6],
        "date": datetime.date.today() - datetime.timedelta(days=12),
    },
    {
        "title": "Write unit tests for API",
        "category": "User Story",
        "prio": "low",
        "status": "awaitFeedback",
        "description": "Ensure all endpoints are covered by tests.",
        "subtasks": [
            {"text": "Test user registration", "status": "checked"},
            {"text": "Test task creation", "status": "unchecked"},
        ],
        "assigned": [7],
        "date": datetime.date.today() - datetime.timedelta(days=5),
    },
    {
        "title": "Add Swagger/OpenAPI documentation",
        "category": "Technical Task",
        "prio": "medium",
        "status": "toDo",
        "description": "Integrate drf-yasg for automatic API docs.",
        "subtasks": [
            {"text": "Install drf-yasg", "status": "checked"},
            {"text": "Configure schema view", "status": "unchecked"},
        ],
        "assigned": [8],
        "date": datetime.date.today() - datetime.timedelta(days=3),
    },
    {
        "title": "Frontend-Backend Integration",
        "category": "User Story",
        "prio": "urgent",
        "status": "inProgress",
        "description": "Connect frontend to backend API and test data flow.",
        "subtasks": [
            {"text": "CORS setup", "status": "checked"},
            {"text": "Test API calls from frontend", "status": "unchecked"},
        ],
        "assigned": [9, 0],
        "date": datetime.date.today() - datetime.timedelta(days=2),
    },
    {
        "title": "Deploy backend locally",
        "category": "Technical Task",
        "prio": "low",
        "status": "toDo",
        "description": "Run backend with manage.py runserver for local testing.",
        "subtasks": [
            {"text": "Check local DB", "status": "unchecked"},
            {"text": "Test endpoints", "status": "unchecked"},
        ],
        "assigned": [1],
        "date": datetime.date.today(),
    },
    {
        "title": "Create admin interface",
        "category": "Technical Task",
        "prio": "medium",
        "status": "done",
        "description": "Register models in Django admin for easy management.",
        "subtasks": [
            {"text": "Register Task model", "status": "checked"},
            {"text": "Register Contact model", "status": "checked"},
        ],
        "assigned": [2, 3],
        "date": datetime.date.today() - datetime.timedelta(days=8),
    },
    {
        "title": "Write project documentation",
        "category": "User Story",
        "prio": "low",
        "status": "awaitFeedback",
        "description": "Document setup, usage, and API for the backend.",
        "subtasks": [
            {"text": "Write README.md", "status": "checked"},
            {"text": "Add API examples", "status": "unchecked"},
        ],
        "assigned": [4, 5],
        "date": datetime.date.today() - datetime.timedelta(days=1),
    },
]

for t in task_templates:
    task = Task.objects.create(
        title=t["title"],
        description=t["description"],
        category=t["category"],
        date=t["date"],
        prio=t["prio"],
        status=t["status"],
    )
    # Assign contacts
    task.assigned_to.set([contacts[i] for i in t["assigned"]])
    # Add subtasks
    for sub in t["subtasks"]:
        Subtask.objects.create(task=task, text=sub["text"], status=sub["status"])

print("10 demo contacts and 10 demo tasks created.")
