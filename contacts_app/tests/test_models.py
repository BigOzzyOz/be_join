from django.test import TestCase
from contacts_app.models import Contact


class ContactModelTest(TestCase):
    def test_create_contact_with_valid_data(self):
        contact = Contact.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            number="+123456789",
            first_letters="JD",
            profile_pic="<svg>...</svg>",
        )
        self.assertEqual(contact.name, "John Doe")
        self.assertEqual(contact.email, "john.doe@example.com")
        self.assertEqual(contact.number, "+123456789")
        self.assertEqual(contact.first_letters, "JD")
        self.assertEqual(contact.profile_pic, "<svg>...</svg>")

    def test_email_uniqueness(self):
        Contact.objects.create(name="John Doe", email="john.doe@example.com")
        with self.assertRaises(Exception):
            Contact.objects.create(name="Jane Doe", email="john.doe@example.com")

    def test_optional_fields(self):
        contact = Contact.objects.create(name="John Doe", email="john.doe@example.com")
        self.assertIsNone(contact.number)
        self.assertIsNone(contact.first_letters)
        self.assertIsNone(contact.profile_pic)

    def test_string_representation(self):
        contact = Contact.objects.create(name="John Doe", email="john.doe@example.com")
        self.assertEqual(str(contact), "John Doe")

    def test_create_contact_with_empty_optional_fields(self):
        contact = Contact.objects.create(name="Empty Fields", email="empty@example.com")
        self.assertIsNone(contact.number)
        self.assertIsNone(contact.first_letters)
        self.assertIsNone(contact.profile_pic)

    def test_contact_string_representation_with_long_name(self):
        contact = Contact.objects.create(name="A" * 255, email="long.name@example.com")
        self.assertEqual(str(contact), "A" * 255)
