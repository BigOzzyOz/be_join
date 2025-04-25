"""
Serializers for the Contact model, including validation and ID-based lookup.
"""

from rest_framework import serializers
from contacts_app.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model, including optional fields for number, initials, and profile picture.
    """

    number = serializers.CharField(required=False, allow_null=True)
    first_letters = serializers.CharField(required=False, allow_null=True)
    profile_pic = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Contact
        fields = ["id", "name", "email", "number", "first_letters", "profile_pic", "is_user"]


class ContactIDSerializer(ContactSerializer):
    """
    Serializer for Contact model, requiring an ID for lookup and validation.
    """

    id = serializers.UUIDField(required=True)

    class Meta:
        model = Contact
        read_only_fields = ["id", "name", "email", "number", "first_letters", "profile_pic"]
        fields = ["id", "name", "email", "number", "first_letters", "profile_pic"]

    def validate_id(self, value):
        """
        Validate that a contact with the given ID exists.
        """
        if not Contact.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Contact with id {value} does not exist.")
        return value
