from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer
from .permissions import IsOwnerOrNonUserOrNotGuest


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrNonUserOrNotGuest]

    def get_queryset(self):
        return Contact.objects.exclude(user__username__in=["guest", "admin"])
