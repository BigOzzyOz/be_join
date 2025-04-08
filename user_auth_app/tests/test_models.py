from django.test import TestCase
from django.contrib.auth.models import User
from contacts_app.models import Contact


class ContactUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="Test@1234")
        self.contact = Contact.objects.get(user=self.user)

    def test_profile_creation(self):
        self.assertEqual(self.contact.user.username, "testuser")
        self.assertEqual(str(self.contact), "testuser")

    def test_profile_uuid(self):
        self.assertIsNotNone(self.contact.id)
        self.assertEqual(self.contact.id, self.contact.pk)
