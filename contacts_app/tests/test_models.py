from django.test import TestCase
from contacts_app.models import Contact


class ContactModelTest(TestCase):
    def test_create_contact_with_valid_data(self):
        contact = Contact.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            number="+123456789",
        )
        contact.refresh_from_db()
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.number, "+123456789")
        expected_initials = "JD"
        self.assertEqual(contact.first_letters, expected_initials)
        self.assertIsNotNone(contact.profile_pic)
        self.assertIn(expected_initials, contact.profile_pic)
        self.assertIn("<svg", contact.profile_pic)

    def test_email_uniqueness(self):
        Contact.objects.create(name="John Doe", email="john.doe@example.com")
        with self.assertRaises(Exception):
            Contact.objects.create(name="Jane Doe", email="john.doe@example.com")

    def test_optional_fields(self):
        contact = Contact.objects.create(name="John Doe", email="john.doe@example.com")
        contact.refresh_from_db()
        self.assertIsNone(contact.number)
        expected_initials = "JD"
        self.assertEqual(contact.first_letters, expected_initials)
        self.assertIsNotNone(contact.profile_pic)
        self.assertIn(expected_initials, contact.profile_pic)

    def test_string_representation(self):
        contact = Contact.objects.create(name="John Doe", email="john.doe@example.com")
        self.assertEqual(str(contact), "John Doe")

    def test_create_contact_with_empty_optional_fields(self):
        contact = Contact.objects.create(name="Empty Fields", email="empty@example.com")
        contact.refresh_from_db()
        self.assertIsNone(contact.number)
        expected_initials = "EF"
        self.assertEqual(contact.first_letters, expected_initials)
        self.assertIsNotNone(contact.profile_pic)
        self.assertIn(expected_initials, contact.profile_pic)

    def test_contact_string_representation_with_long_name(self):
        long_name = "A" * 255
        contact = Contact.objects.create(name=long_name, email="long.name@example.com")
        self.assertEqual(str(contact), long_name)
        contact.refresh_from_db()
        self.assertEqual(contact.first_letters, "A")
