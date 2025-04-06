from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from user_auth_app.models import ProfileUser


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
            "email": "newuser@example.com",
            "name": "New User",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "newuser@example.com")
        self.assertEqual(response.data["email"], "newuser@example.com")

    def test_user_registration_password_mismatch(self):
        data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "Test@1234",
            "repeated_password": "Mismatch1234",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Passwords do not match.", str(response.data))

    def test_user_registration_duplicate_email(self):
        User.objects.create_user(username="testuser@example.com", email="testuser@example.com", password="Test@1234")
        data = {
            "email": "testuser@example.com",
            "name": "New User",
            "password": "Test@1234",
            "repeated_password": "Test@1234",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Email already exists.", str(response.data))


class GuestUserViewTest(APITestCase):
    def setUp(self):
        self.guest_url = "/auth/guest/"

    def test_guest_user_creation(self):
        response = self.client.post(self.guest_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["username"], "guest")
        self.assertTrue(User.objects.filter(username="guest").exists())
        self.assertTrue(ProfileUser.objects.filter(user__username="guest").exists())

    def test_guest_user_reuse(self):
        User.objects.create_user(username="guest", password="guest")
        first_login_response = self.client.post(self.guest_url, format="json")
        self.assertEqual(first_login_response.status_code, status.HTTP_201_CREATED)
        second_login_response = self.client.post(self.guest_url, format="json")
        self.assertEqual(second_login_response.status_code, status.HTTP_200_OK)
        self.assertIn("token", second_login_response.data)
        self.assertEqual(second_login_response.data["username"], "guest")
        self.assertEqual(User.objects.filter(username="guest").count(), 1)
        self.assertEqual(ProfileUser.objects.filter(user__username="guest").count(), 1)
