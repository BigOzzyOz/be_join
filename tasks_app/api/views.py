from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import SAFE_METHODS
from tasks_app.models import Task
from tasks_app.api.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SummaryView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        if request.method not in SAFE_METHODS:
            return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        tasks = self.get_queryset()
        if not tasks.exists():
            return Response({"error": "No tasks found"}, status=status.HTTP_404_NOT_FOUND)
        data = {
            "todos": tasks.filter(status="toDo").count(),
            "in_progress": tasks.filter(status="inProgress").count(),
            "await_feedback": tasks.filter(status="awaitFeedback").count(),
            "done": tasks.filter(status="done").count(),
            "total": tasks.count(),
            "urgent": tasks.filter(prio="urgent").count(),
        }
        return Response(data)
