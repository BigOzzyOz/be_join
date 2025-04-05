from django.test import TestCase
from django.contrib.auth.models import User
from user_auth_app.models import ProfileUser


class ProfileUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.profile = ProfileUser.objects.get(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(str(self.profile), "testuser")

    def test_profile_uuid(self):
        self.assertIsNotNone(self.profile.id)
        self.assertEqual(self.profile.id, self.profile.pk)
