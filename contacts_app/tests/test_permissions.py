from django.test import TestCase
from django.contrib.auth.models import User
from contacts_app.models import Contact
from contacts_app.api.permissions import IsOwnerOrNonUserOrNotGuest
from rest_framework.test import APIRequestFactory


class IsOwnerOrNonUserOrNotGuestTests(TestCase):
    def setUp(self):
        # Testdaten erstellen
        self.factory = APIRequestFactory()
        self.permission = IsOwnerOrNonUserOrNotGuest()

        self.user_owner = User.objects.create_user(username="owner", password="password")
        self.user_guest = User.objects.create_user(username="guest", password="password")
        self.user_other = User.objects.create_user(username="other", password="password")

        # Kontakt des Besitzers abrufen (wird durch Signal erstellt)
        self.contact_owned = self.user_owner.contact

        # Kontakt ohne Benutzer manuell erstellen
        self.contact_no_user = Contact.objects.create(
            name="No User Contact", email="nouser@example.com", user=None, is_user=False
        )

    def test_owner_has_permission(self):
        # Der Besitzer des Kontakts hat Zugriff
        request = self.factory.delete("/")
        request.user = self.user_owner
        self.assertTrue(self.permission.has_object_permission(request, None, self.contact_owned))

    def test_non_user_contact_has_permission(self):
        # Kontakte ohne zugewiesenen Benutzer können bearbeitet werden
        request = self.factory.delete("/")
        request.user = self.user_other
        self.assertTrue(self.permission.has_object_permission(request, None, self.contact_no_user))

    def test_guest_user_no_permission(self):
        # Gast-Benutzer hat keinen Zugriff
        request = self.factory.delete("/")
        request.user = self.user_guest
        self.assertFalse(self.permission.has_object_permission(request, None, self.contact_owned))

    def test_other_user_no_permission_on_owned_contact(self):
        # Ein anderer Benutzer (kein Gast) hat keinen Zugriff auf fremde Kontakte
        request = self.factory.delete("/")
        request.user = self.user_other
        self.assertFalse(self.permission.has_object_permission(request, None, self.contact_owned))

    def test_safe_methods_always_allowed(self):
        # SAFE_METHODS (GET, HEAD, OPTIONS) sind immer erlaubt
        request = self.factory.get("/")
        request.user = self.user_other
        self.assertTrue(self.permission.has_object_permission(request, None, self.contact_owned))
