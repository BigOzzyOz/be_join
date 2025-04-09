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

    def test_contact_data_updated_on_user_update(self):
        user = User.objects.create_user(
            username="testuser", first_name="test", last_name="user", email="testuser@example.com", password="Test@1234"
        )
        profile = Contact.objects.get(user=user)
        user.email = "newmail@example.com"
        user.first_name = "new"
        user.last_name = "name"
        user.save()
        profile.refresh_from_db()
        self.assertEqual(profile.email, "newmail@example.com")
        self.assertEqual(profile.name, "new name")

    def test_change_contact_on_delete_user(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        contact = Contact.objects.get(user=user)
        user.delete()
        contact.refresh_from_db()
        self.assertFalse(contact.is_user)
        self.assertIsNone(contact.user)


class ContactSignalExceptionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        self.contact = Contact.objects.get(user=self.user)

    @patch("user_auth_app.signals.logger.error")
    def test_update_signal_exception_handling(self, mock_logger):
        with patch("contacts_app.models.Contact.objects.filter", side_effect=Exception("Simulated error")):
            self.user.first_name = "Updated"
            self.user.save()

        mock_logger.assert_called_once_with("Error in create_or_update_contact signal: Simulated error")

    @patch("user_auth_app.signals.logger.error")
    def test_delete_signal_exception(self, mock_logger):
        with patch("contacts_app.models.Contact.objects.filter", side_effect=Exception("Simulated error")):
            self.user.delete()

        mock_logger.assert_called_once_with("Error in delete_user_tag_in_contact signal: Simulated error")
