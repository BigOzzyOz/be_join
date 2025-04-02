from rest_framework import serializers
from contacts_app.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(required=False)

    class Meta:
        model = Contact
        fields = ["id", "name", "mail", "number", "first_letters", "profile_pic"]
        read_only_fields = ["id", "first_letters", "profile_pic"]

    def validate(self, data):
        print("Validation method called")
        contact_id = data.get("id")
        if not Contact.objects.filter(id=contact_id).exists():
            raise serializers.ValidationError(f"Contact with id {contact_id} does not exist.")
        return data


class ContactIDSerializer(ContactSerializer):
    class Meta:
        model = Contact
        read_only_fields = ["id", "name", "mail", "number", "first_letters", "profile_pic"]
        fields = ["id", "name", "mail", "number", "first_letters", "profile_pic"]
