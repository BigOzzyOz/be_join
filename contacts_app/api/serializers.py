from rest_framework import serializers
from contacts_app.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    number = serializers.CharField(required=False, allow_null=True)
    first_letters = serializers.CharField(required=False, allow_null=True)
    profile_pic = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = Contact
        fields = ["id", "name", "mail", "number", "first_letters", "profile_pic"]

    def validate_mail(self, value):
        return value


class ContactIDSerializer(ContactSerializer):
    id = serializers.UUIDField(required=True)

    class Meta:
        model = Contact
        read_only_fields = ["id", "name", "mail", "number", "first_letters", "profile_pic"]
        fields = ["id", "name", "mail", "number", "first_letters", "profile_pic"]

    def validate_id(self, value):
        if not Contact.objects.filter(id=value).exists():
            raise serializers.ValidationError(f"Contact with id {value} does not exist.")
        return value
