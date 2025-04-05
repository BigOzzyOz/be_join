from django.test import TestCase
from django.contrib.auth.models import User
from user_auth_app.models import ProfileUser


class UserProfileSignalTest(TestCase):
    def test_profile_created_on_user_creation(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.assertTrue(ProfileUser.objects.filter(user=user).exists())

    def test_profile_saved_on_user_save(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        profile = ProfileUser.objects.get(user=user)
        user.save()
        profile.refresh_from_db()
        self.assertEqual(profile.user, user)
