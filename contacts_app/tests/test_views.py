from rest_framework.test import APITestCase
from rest_framework import status
from contacts_app.models import Contact
from django.urls import reverse


class ContactViewSetTest(APITestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name="John Doe",
            mail="john.doe@example.com",
            number="+123456789",
            first_letters="JD",
            profile_pic="<svg>...</svg>",
        )
        self.list_url = reverse("contact-list")

    def test_list_contacts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John Doe")

    def test_retrieve_contact(self):
        url = reverse("contact-detail", args=[self.contact.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Doe")

    def test_create_contact(self):
        data = {
            "name": "Jane Doe",
            "mail": "jane.doe@example.com",
            "number": "+987654321",
            "first_letters": "JD",
            "profile_pic": "<svg>...</svg>",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)
        self.assertEqual(Contact.objects.last().name, "Jane Doe")

    def test_update_contact(self):
        url = reverse("contact-detail", args=[self.contact.id])
        data = {
            "name": "John Updated",
            "mail": "john.doe@example.com",
            "number": "+987654321",
            "first_letters": "JU",
            "profile_pic": "<svg>Updated</svg>",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.name, "John Updated")
        self.assertEqual(self.contact.number, "+987654321")

    def test_delete_contact(self):
        url = reverse("contact-detail", args=[self.contact.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contact.objects.count(), 0)

    def test_create_contact_with_duplicate_email(self):
        data = {
            "name": "Duplicate Email",
            "mail": "john.doe@example.com",
            "number": "+123456789",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mail", response.data)
