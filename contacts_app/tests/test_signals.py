from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from contacts_app.models import Contact


class ContactSignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        self.contact = Contact.objects.get(user=self.user)

    @patch("contacts_app.signals.logger.error")
    def test_create_update_contact_profile_signal(self, mock_logger):
        self.contact.email = "newemail@example.com"
        self.contact.name = "New Name"
        self.contact.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Name")

        mock_logger.assert_not_called()

    @patch("contacts_app.signals.logger.error")
    @patch("django.db.models.query.QuerySet.update")
    def test_create_update_contact_profile_signal_exception(self, mock_update, mock_logger):
        mock_update.side_effect = Exception("Simulated error")

        self.contact.email = "newemail@example.com"
        self.contact.save()

        mock_logger.assert_called_once_with("Error creating/updating contact profile: Simulated error")

    @patch("contacts_app.signals.logger.error")
    def test_delete_contact_profile_signal(self, mock_logger):
        self.contact.delete()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)

        mock_logger.assert_not_called()

    @patch("contacts_app.signals.logger.error")
    def test_delete_contact_profile_signal_exception(self, mock_logger):
        with patch.object(User, "delete", side_effect=Exception("Simulated error")):
            self.contact.delete()

        mock_logger.assert_called_once_with("Error deleting contact profile: Simulated error")
