from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth_app.models import ProfileUser


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model: ProfileUser
        fields = ("id", "user")


class RegisterSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField()

    class Meta:
        model = User
        fields = ("username", "email", "password", "repeated_password")
        extra_kwargs = {
            "password": {"write_only": True},
            "repeated_password": {"write_only": True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
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
        password = data.get("password")
        repeated_password = data.get("repeated_password")

        if password != repeated_password:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def save(self):
        password = self.validated_data["password"]
        email = self.validated_data["email"]
        username = self.validated_data["username"]
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return user
