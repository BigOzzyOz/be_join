"""
Serializers for user registration and validation logic.
"""

from rest_framework import serializers
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, including password validation and duplicate email checks.
    """

    repeated_password = serializers.CharField()
    name = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("email", "name", "password", "repeated_password")
        extra_kwargs = {
            "password": {"write_only": True},
            "repeated_password": {"write_only": True},
        }

    def validate_email(self, value):
        """
        Ensure the email is unique in the User model.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        """
        Validate password for length, digits, letters, case, and special characters.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one digit.")
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        if not any(char.islower() for char in value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        if not any(char in "!@#$%^&*()-_+=<>?/|{}[]:;'" for char in value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value

    def validate(self, data):
        """
        Ensure password and repeated_password match.
        """
        password = data.get("password")
        repeated_password = data.get("repeated_password")

        if password != repeated_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        """
        Create and save a new User instance with validated data.
        """
        login = self.validated_data["email"].lower()
        name = self.validated_data["name"]
        password = self.validated_data["password"]
        user = User(
            username=login,
            email=login,
            first_name=name.split()[0] if name else "",
            last_name=name.split()[1] if len(name.split()) > 1 else "",
        )
        user.set_password(password)
        user.save()

        return user
