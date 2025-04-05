from django.urls import path
from rest_framework.routers import SimpleRouter
from tasks_app.api.views import TaskViewSet, SummaryView

router = SimpleRouter()
router.register(r"", TaskViewSet, basename="task")

urlpatterns = [
    path("summary/", SummaryView.as_view(), name="task-summary"),
]

urlpatterns += router.urls
