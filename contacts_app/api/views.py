from rest_framework.viewsets import ModelViewSet
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer

    def get_queryset(self):
        return Contact.objects.exclude(name__in=["guest", "admin"])
