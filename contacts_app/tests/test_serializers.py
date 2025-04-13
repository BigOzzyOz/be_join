from django.test import TestCase
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer, ContactIDSerializer


class ContactSerializerTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="John Doe",
            email="john.doe@example.com",
            number="+123456789",
        )
        self.contact.refresh_from_db()

    def test_serialize_contact(self):
        serializer = ContactSerializer(self.contact)
        expected_data = {
            "id": str(self.contact.id),
            "name": "John Doe",
            "email": "john.doe@example.com",
            "number": "+123456789",
            "first_letters": "JD",
            "profile_pic": self.contact.profile_pic,
        }
        self.assertEqual(serializer.data["id"], expected_data["id"])
        self.assertEqual(serializer.data["name"], expected_data["name"])
        self.assertEqual(serializer.data["email"], expected_data["email"])
        self.assertEqual(serializer.data["number"], expected_data["number"])
        self.assertEqual(serializer.data["first_letters"], expected_data["first_letters"])
        self.assertIsNotNone(serializer.data["profile_pic"])
        self.assertIn("<svg", serializer.data["profile_pic"])
        self.assertIn("JD", serializer.data["profile_pic"])

    def test_validate_contact_with_valid_id(self):
        data = {"id": str(self.contact.id)}
        serializer = ContactIDSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_validate_contact_with_invalid_id(self):
        data = {"id": "invalid-uuid-format"}
        serializer = ContactIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("id", serializer.errors)
        self.assertIn("Must be a valid UUID.", str(serializer.errors["id"][0]))

        non_existent_uuid = "123e4567-e89b-12d3-a456-426614174000"
        data = {"id": non_existent_uuid}
        serializer = ContactIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("id", serializer.errors)
        self.assertIn(f"Contact with id {non_existent_uuid} does not exist.", str(serializer.errors["id"][0]))

    def test_validate_contact_without_id(self):
        data = {}
        serializer = ContactIDSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("id", serializer.errors)

    def test_optional_fields(self):
        data = {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
        }
        serializer = ContactSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        instance = serializer.save()
        instance.refresh_from_db()
        self.assertEqual(instance.first_letters, "JD")
        self.assertIsNotNone(instance.profile_pic)

    def test_invalid_email(self):
        data = {
            "name": "John Doe",
            "email": "invalid-email",
            "number": "+123456789",
        }
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_update_existing_contact(self):
        data = {
            "name": "John Doe Updated",
            "email": "john.update@example.com",
            "number": "+987654321",
        }
        serializer = ContactSerializer(instance=self.contact, data=data, partial=True)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_contact = serializer.save()
        updated_contact.refresh_from_db()
        self.assertEqual(updated_contact.name, "John Doe Updated")
        self.assertEqual(updated_contact.email, "john.update@example.com")
        self.assertEqual(updated_contact.number, "+987654321")
        expected_initials = "JU"
        self.assertEqual(updated_contact.first_letters, expected_initials)
        self.assertIsNotNone(updated_contact.profile_pic)
        self.assertIn(expected_initials, updated_contact.profile_pic)

    def test_create_contact_with_missing_required_fields(self):
        data = {"name": "Missing Email"}
        serializer = ContactSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)
