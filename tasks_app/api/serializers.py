"""
Serializers for Task and Subtask models, including validation and nested handling.
"""

from rest_framework import serializers
from tasks_app.models import Task, Subtask
from contacts_app.api.serializers import ContactIDSerializer
from contacts_app.models import Contact


class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Subtask model, including ID, text, and status fields.
    """

    id = serializers.UUIDField(required=False)

    class Meta:
        model = Subtask
        fields = ["id", "text", "status"]
        read_only_fields = ["id"]


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model, including nested subtasks and assigned contacts.
    Handles creation, update, and validation of related objects.
    """

    id = serializers.UUIDField(required=False)
    subtasks = SubtaskSerializer(many=True, allow_empty=True, default=[])
    assigned_to = ContactIDSerializer(many=True, allow_empty=True, default=[])
    prio_display = serializers.CharField(source="get_prio_display", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "category",
            "date",
            "prio",
            "prio_display",
            "status",
            "status_display",
            "assigned_to",
            "subtasks",
        ]
        read_only_fields = ["id", "prio_display", "status_display"]

    def validate_subtasks(self, value):
        """
        Ensure subtasks value is a list or empty.
        """
        if value is None or value == []:
            return []
        return value

    def validate_assigned_to(self, value):
        """
        Ensure assigned_to value is a list of contacts with IDs.
        """
        if value is None or value == []:
            return []
        for contact in value:
            if not contact or "id" not in contact:
                raise serializers.ValidationError("Each contact must include an 'id' field.")
        return value

    def handle_subtasks(self, instance, subtasks_data):
        """
        Create, update, or delete subtasks for a given task instance.
        """
        existing_subtask_ids = set(instance.subtasks.values_list("id", flat=True))
        new_subtask_ids = set()

        for subtask_data in subtasks_data:
            subtask_id = subtask_data.get("id")
            if subtask_id:
                new_subtask_ids.add(self.update_existing_subtask(subtask_id, subtask_data))
            else:
                new_subtask_ids.add(self.create_new_subtask(instance, subtask_data))

        removed_subtask_ids = existing_subtask_ids - new_subtask_ids
        self.delete_removed_subtasks(removed_subtask_ids)

    def update_existing_subtask(self, subtask_id, subtask_data):
        """
        Update an existing subtask with new data.
        """
        subtask_instance = Subtask.objects.get(id=subtask_id)
        subtask_instance.text = subtask_data.get("text", subtask_instance.text)
        subtask_instance.status = subtask_data.get("status", subtask_instance.status)
        subtask_instance.save()
        return subtask_id

    def create_new_subtask(self, instance, subtask_data):
        """
        Create a new subtask for a given task instance.
        """
        new_subtask = Subtask.objects.create(task=instance, **subtask_data)
        return new_subtask.id

    def delete_removed_subtasks(self, removed_subtask_ids):
        """
        Delete subtasks that are no longer present in the updated data.
        """
        for subtask_id in removed_subtask_ids:
            Subtask.objects.get(id=subtask_id).delete()

    def handle_assigned_to(self, instance, assigned_to_data):
        """
        Set the assigned contacts for a task instance.
        """
        if not assigned_to_data:
            instance.assigned_to.set([])
            return
        instance.assigned_to.clear()
        for contact_data in assigned_to_data:
            contact_id = contact_data.get("id")
            contact = Contact.objects.get(id=contact_id)
            instance.assigned_to.add(contact)

    def create(self, validated_data):
        """
        Create a new Task instance with nested subtasks and assigned contacts.
        """
        subtasks_data = validated_data.pop("subtasks", [])
        assigned_to_data = validated_data.pop("assigned_to", [])
        task = Task.objects.create(**validated_data)

        self.handle_subtasks(task, subtasks_data)
        self.handle_assigned_to(task, assigned_to_data)

        task.save()
        return task

    def update(self, instance, validated_data):
        """
        Update a Task instance with nested subtasks and assigned contacts.
        """
        subtasks_data = validated_data.pop("subtasks", [])
        assigned_to_data = validated_data.pop("assigned_to", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        self.handle_subtasks(instance, subtasks_data)
        self.handle_assigned_to(instance, assigned_to_data)

        instance.save()
        return instance
