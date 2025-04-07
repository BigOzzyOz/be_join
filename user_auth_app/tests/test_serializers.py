from django.test import TestCase
from django.contrib.auth.models import User
from contacts_app.models import Contact
from user_auth_app.models import ProfileUser
from user_auth_app.api.serializers import RegisterSerializer


class RegisterSerializerTest(TestCase):
    def test_valid_registration(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Test@1234",
            "repeated_password": "Mismatch1234",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_duplicate_email(self):
        User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        data = {
            "username": "newuser",
            "email": "testuser@example.com",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_contact_created_on_user_registration(self):
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        contact = Contact.objects.get(email="newuser@example.com")
        self.assertEqual(contact.name, "New User")
        self.assertEqual(contact.email, "newuser@example.com")
        self.assertEqual(contact.number, "Please add your number")
        self.assertEqual(contact.is_user, True)
        self.assertIsNotNone(contact.profile_pic)

    def test_contact_updated_on_user_registration(self):
        contact = Contact.objects.create(
            name="Old Name",
            email="existing@example.com",
            number="Old Number",
            is_user=False,
        )

        data = {
            "email": "existing@example.com",
            "name": "Updated User",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        contact.refresh_from_db()
        self.assertEqual(contact.name, "Updated User")
        self.assertEqual(contact.email, "existing@example.com")
        self.assertEqual(contact.number, "Please add your number")
        self.assertEqual(contact.is_user, True)
        self.assertIsNotNone(contact.profile_pic)

    def test_contact_first_letters_generated_correctly(self):
        data = {
            "email": "newuser@example.com",
            "name": "John Doe",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()

        contact = Contact.objects.get(email="newuser@example.com")
        self.assertEqual(contact.first_letters, "JD")


class RegisterSerializerValidationTest(TestCase):
    def test_validate_email_already_exists(self):
        User.objects.create_user(username="existinguser", email="existing@example.com", password="Test@1234")
        data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
        self.assertEqual(serializer.errors["email"][0], "Email already exists.")

    def test_validate_password_too_short(self):
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "Short1!",
            "repeated_password": "Short1!",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "Password must be at least 8 characters long.")

    def test_validate_password_missing_digit(self):
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "Password!",
            "repeated_password": "Password!",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "Password must contain at least one digit.")

    def test_validate_password_missing_letter(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "12345678!",
            "repeated_password": "12345678!",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "Password must contain at least one letter.")

    def test_validate_password_missing_uppercase(self):
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "password1!",
            "repeated_password": "password1!",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "Password must contain at least one uppercase letter.")

    def test_validate_password_missing_lowercase(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "PASSWORD1!",
            "repeated_password": "PASSWORD1!",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "Password must contain at least one lowercase letter.")

    def test_validate_password_missing_special_character(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Password1",
            "repeated_password": "Password1",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password", serializer.errors)
        self.assertEqual(serializer.errors["password"][0], "Password must contain at least one special character.")

    def test_validate_password_mismatch(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "Password1!",
            "repeated_password": "Mismatch1!",
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Passwords do not match.")
