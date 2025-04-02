from rest_framework.routers import SimpleRouter
from contacts_app.api.views import ContactViewSet

router = SimpleRouter()
router.register(r"", ContactViewSet, basename="contact")

urlpatterns = router.urls
