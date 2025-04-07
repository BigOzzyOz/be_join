from rest_framework.viewsets import ModelViewSet
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer


class ContactViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    lookup_field = "id"
