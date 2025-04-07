from django.test import TestCase
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer, ContactIDSerializer


class ContactSerializerTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            number="+123456789",
            first_letters="JD",
            profile_pic="<svg>...</svg>",
        )

    def test_serialize_contact(self):
        serializer = ContactSerializer(self.contact)
        expected_data = {
            "id": str(self.contact.id),
            "name": "John Doe",
            "email": "john.doe@example.com",
            "number": "+123456789",
            "first_letters": "JD",
            "profile_pic": "<svg>...</svg>",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_validate_contact_with_valid_id(self):
        data = {"id": str(self.contact.id)}
        serializer = ContactIDSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_validate_contact_with_invalid_id(self):
        data = {"id": "123e4567-e89b-12d3-a456-426614174000"}
        serializer = ContactIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("id", serializer.errors)

    def test_validate_contact_without_id(self):
        data = {}
        serializer = ContactIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("id", serializer.errors)

    def test_optional_fields(self):
        data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "number": None,
            "first_letters": None,
            "profile_pic": None,
        }
        serializer = ContactSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        data = {
            "id": str(self.contact.id),
            "name": "John Doe",
            "email": "invalid-email",
            "number": "+123456789",
            "first_letters": "JD",
            "profile_pic": "<svg>...</svg>",
        }
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_update_existing_contact(self):
        data = {
            "name": "John Doe Updated",
            "email": "john.doe@example.com",
            "number": "+987654321",
            "first_letters": "JD",
            "profile_pic": "<svg>Updated</svg>",
        }
        serializer = ContactSerializer(instance=self.contact, data=data)
        self.assertTrue(serializer.is_valid())
        updated_contact = serializer.save()
        self.assertEqual(updated_contact.name, "John Doe Updated")
        self.assertEqual(updated_contact.number, "+987654321")
        self.assertEqual(updated_contact.profile_pic, "<svg>Updated</svg>")

    def test_create_contact_with_missing_required_fields(self):
        data = {"name": "Missing Email"}
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_create_contact_with_invalid_phone_number(self):
        data = {
            "name": "Invalid Phone",
            "email": "invalid.phone@example.com",
            "number": "invalid-phone",
        }
        serializer = ContactSerializer(data=data)
        self.assertTrue(serializer.is_valid())
