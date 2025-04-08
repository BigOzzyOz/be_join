from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from contacts_app.models import Contact


class UserSignalTest(TestCase):
    def test_contact_created_on_user_creation(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.assertTrue(Contact.objects.filter(user=user).exists())

    def test_contact_saved_on_user_save(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        profile = Contact.objects.get(user=user)
        user.save()
        profile.refresh_from_db()
        self.assertEqual(profile.user, user)

    def test_change_contact_on_delete_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        contact = Contact.objects.get(user=user)
        user.delete()
        contact.refresh_from_db()
        self.assertFalse(contact.is_user)
        self.assertIsNone(contact.user)


class ContactSignalExceptionTest(TestCase):
    @patch("contacts_app.models.Contact.objects.filter")
    def test_signal_exception_handling(self, mock_filter):
        mock_filter.side_effect = Exception("Simulated error")

        try:
            User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        except Exception as e:
            self.fail(f"Signal raised an exception: {e}")

        self.assertTrue(mock_filter.called)
