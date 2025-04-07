from rest_framework import serializers
from django.contrib.auth.models import User
from contacts_app.models import Contact
from user_auth_app.models import ProfileUser
from contacts_app.utils import generate_svg_circle_with_initials


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model: ProfileUser
        fields = ("id", "user")


class RegisterSerializer(serializers.ModelSerializer):
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

        contact, created = Contact.objects.update_or_create(
            email=user.email,
            defaults={
                "id": ProfileUser.objects.get(user=user).id,
                "name": f"{user.first_name} {user.last_name}",
                "number": "Please add your number",
                "email": user.email,
                "first_letters": "".join(
                    [name[0].upper() for name in f"{user.first_name} {user.last_name}".split() if name]
                ),
                "is_user": True,
                "profile_pic": generate_svg_circle_with_initials(f"{user.first_name} {user.last_name}"),
            },
        )

        return user
