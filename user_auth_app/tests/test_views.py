from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserAuthViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.login_url = "/auth/login/"
        self.register_url = "/auth/register/"

    def test_user_login_success(self):
        data = {"username": "testuser", "password": "Test@1234"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_user_login_invalid_credentials(self):
        data = {"username": "testuser", "password": "WrongPassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_user_registration_success(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_user_registration_password_mismatch(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Test@1234",
            "repeated_password": "Mismatch1234",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match.", str(response.data))

    def test_user_registration_duplicate_email(self):
        data = {
            "username": "newuser",
            "email": "testuser@example.com",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email already exists.", str(response.data))
