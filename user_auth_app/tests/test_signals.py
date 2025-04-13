from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch
from contacts_app.models import Contact


class UserSignalTest(TestCase):
    def test_contact_created_on_user_creation(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.assertTrue(Contact.objects.filter(user=user).exists())
        contact = Contact.objects.get(user=user)
        self.assertEqual(contact.name, "testuser")
        self.assertEqual(contact.first_letters, "T")

    def test_contact_created_with_name_on_user_creation(self):
        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        self.assertTrue(Contact.objects.filter(user=user).exists())
        contact = Contact.objects.get(user=user)
        self.assertEqual(contact.name, "Test User")
        self.assertEqual(contact.first_letters, "TU")

    def test_contact_updated_on_user_update(self):
        user = User.objects.create_user(
            username="testuser", first_name="test", last_name="user", email="testuser@example.com", password="Test@1234"
        )
        contact = Contact.objects.get(user=user)
        self.assertEqual(contact.email, "testuser@example.com")
        self.assertEqual(contact.name, "test user")
        self.assertEqual(contact.first_letters, "TU")

        user.email = "newmail@example.com"
        user.first_name = "New"
        user.last_name = "Name"
        user.save()

        contact.refresh_from_db()
        self.assertEqual(contact.email, "newmail@example.com")
        self.assertEqual(contact.name, "New Name")
        self.assertEqual(contact.first_letters, "NN")
        self.assertTrue(contact.is_user)
        self.assertEqual(contact.user, user)

    def test_contact_updated_when_user_created_and_contact_exists(self):
        existing_contact = Contact.objects.create(email="testuser@example.com", name="Old Name", number="12345")
        self.assertFalse(existing_contact.is_user)
        self.assertIsNone(existing_contact.user)

        user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="Test@1234", first_name="Test", last_name="User"
        )

        existing_contact.refresh_from_db()
        self.assertEqual(existing_contact.name, "Test User")
        self.assertEqual(existing_contact.first_letters, "TU")
        self.assertTrue(existing_contact.is_user)
        self.assertEqual(existing_contact.user, user)
        self.assertEqual(existing_contact.number, "12345")

        self.assertEqual(Contact.objects.filter(email="testuser@example.com").count(), 1)

    def test_contact_dissociated_on_user_delete(self):
        user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        contact = Contact.objects.get(user=user)
        user.delete()
        contact.refresh_from_db()
        self.assertFalse(contact.is_user)
        self.assertIsNone(contact.user)
        self.assertEqual(contact.email, "testuser@example.com")
        self.assertEqual(contact.name, "testuser")


class ContactSignalLoggingTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="logtestuser",
            email="logtest@example.com",
            password="Test@1234",
            first_name="Log",
            last_name="User",
        )

    @patch("user_auth_app.signals.logger.error")
    def test_update_signal_exception_logging(self, mock_logger_error):
        with patch(
            "user_auth_app.signals._calculate_contact_attributes", side_effect=Exception("Simulated update error")
        ):
            self.user.first_name = "Updated"
            try:
                self.user.save()
            except Exception:
                pass

        expected_message = f"Error in signal for user {self.user.username}: Simulated update error"
        mock_logger_error.assert_called_once_with(expected_message)

    @patch("user_auth_app.signals.logger.error")
    def test_delete_signal_exception_logging(self, mock_logger_error):
        with patch("contacts_app.models.Contact.objects.filter", side_effect=Exception("Simulated delete error")):
            try:
                self.user.delete()
            except Exception:
                pass

        expected_message = f"Error in pre_delete signal for user {self.user.username}: Simulated delete error"
        mock_logger_error.assert_called_once_with(expected_message)

    @patch("contacts_app.signals.logger.warning")
    @patch("user_auth_app.signals.logger.info")
    def test_delete_user_without_contact_logs_info(self, mock_logger_info, mock_contact_warning):
        try:
            contact_to_delete = Contact.objects.get(user=self.user)
            contact_to_delete.delete()
        except Contact.DoesNotExist:
            self.fail("Contact associated with self.user not found in setUp.")

        self.user.delete()

        mock_contact_warning.assert_called_once()
