from rest_framework.routers import SimpleRouter
from tasks_app.api.views import TaskViewSet

router = SimpleRouter()
router.register(r"", TaskViewSet, basename="task")

urlpatterns = router.urls
