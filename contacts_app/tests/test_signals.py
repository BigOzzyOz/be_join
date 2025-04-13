from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth.models import User
from contacts_app.models import Contact
from django.db.models.signals import post_save
from contacts_app.signals import update_contact_visuals, create_update_contact_profile


class ContactUserSyncSignalTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="Test@1234", first_name="Test", last_name="User"
        )
        self.contact = Contact.objects.get(user=self.user)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "Test User")
        self.assertEqual(self.contact.email, "testuser@example.com")
        self.assertTrue(self.contact.is_user)

    def test_user_updated_on_contact_change(self):
        self.contact.email = "newemail@example.com"
        self.contact.name = "New Name"
        self.contact.save()

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "newemail@example.com")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "Name")

    @patch("contacts_app.signals.logger.error")
    @patch("django.contrib.auth.models.User.objects.filter")
    def test_create_update_profile_exception_logging(self, mock_user_filter, mock_logger):
        mock_qs = mock_user_filter.return_value
        mock_qs.update.side_effect = Exception("Simulated DB error")

        post_save.disconnect(update_contact_visuals, sender=Contact)
        try:
            self.contact.email = "another@example.com"
            self.contact.save()
        finally:
            post_save.connect(update_contact_visuals, sender=Contact)

        mock_logger.assert_called_once_with("Error creating/updating contact profile: Simulated DB error")
        self.user.refresh_from_db()
        self.assertNotEqual(self.user.email, "another@example.com")

    @patch("contacts_app.signals.logger.warning")
    def test_user_deleted_on_contact_delete(self, mock_logger_warning):
        user_id = self.user.id

        self.contact.delete()

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)

        mock_logger_warning.assert_called_once()

    @patch("contacts_app.signals.logger.error")
    @patch("django.contrib.auth.models.User.delete")
    def test_delete_associated_user_exception_logging(self, mock_user_delete, mock_logger_error):
        mock_user_delete.side_effect = Exception("Simulated delete error")
        contact_pk = self.contact.pk

        self.contact.delete()

        expected_error = f"Error deleting user associated with contact {contact_pk}: Simulated delete error"
        mock_logger_error.assert_called_once_with(expected_error)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    @patch("contacts_app.signals.logger.warning")
    @patch("django.contrib.auth.models.User.delete")
    def test_delete_non_user_contact_does_not_delete_user(self, mock_user_delete, mock_logger_warning):
        non_user_contact = Contact.objects.create(name="Guest Contact", email="guest@example.com", is_user=False)

        non_user_contact.delete()

        mock_user_delete.assert_not_called()
        for c_args, c_kwargs in mock_logger_warning.call_args_list:
            self.assertNotIn("Deleted user", c_args[0])
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())


class ContactVisualsSignalTests(TestCase):
    def setUp(self):
        post_save.disconnect(create_update_contact_profile, sender=Contact)
        self.contact = Contact.objects.create(
            name="Initial Name",
            email="visual@example.com",
        )
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.first_letters, "IN")

    def tearDown(self):
        post_save.connect(create_update_contact_profile, sender=Contact)

    def test_visuals_updated_on_name_change(self):
        expected_letters = "NN"
        expected_pic_content = "NN"

        self.contact.name = "New Name"
        self.contact.save()

        self.contact.refresh_from_db()

        self.assertEqual(self.contact.first_letters, expected_letters)
        self.assertIsNotNone(self.contact.profile_pic)
        self.assertIn("<svg", self.contact.profile_pic)
        self.assertIn(expected_pic_content, self.contact.profile_pic)

    def test_visuals_save_not_called_if_no_change(self):
        self.contact.refresh_from_db()
        initial_name = "Initial Name"
        self.assertEqual(self.contact.name, initial_name)
        self.assertEqual(self.contact.first_letters, "IN")
        self.assertIsNotNone(self.contact.profile_pic)
        db_pic = self.contact.profile_pic

        with patch("contacts_app.models.Contact.save") as mock_save_method:
            self.contact.save()

            mock_save_method.assert_called_once()

            call_args, call_kwargs = mock_save_method.call_args
            self.assertNotIn(
                "update_fields",
                call_kwargs,
                "save() wurde mit update_fields aufgerufen, was auf einen unnötigen internen Signal-Aufruf hindeutet.",
            )

        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, initial_name)
        self.assertEqual(self.contact.first_letters, "IN")
        self.assertEqual(self.contact.profile_pic, db_pic)

    @patch("contacts_app.signals.logger.error")
    @patch("contacts_app.utils.get_initials_from_name")
    def test_visuals_update_exception_logging(self, mock_get_initials, mock_logger):
        mock_get_initials.side_effect = Exception("Simulated initials error")
        contact_pk = self.contact.pk

        self.contact.name = "Error Name"
        self.contact.save()

        expected_error_message = f"Error updating contact visuals for contact {contact_pk}: Simulated initials error"
        mock_logger.assert_called_once_with(expected_error_message, exc_info=True)
