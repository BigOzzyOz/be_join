from rest_framework.viewsets import ModelViewSet
from tasks_app.models import Task
from tasks_app.api.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
