from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from tasks_app.models import Task
from tasks_app.api.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SummaryView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        if not tasks.exists():
            return Response({"error": "No tasks found"}, status=status.HTTP_404_NOT_FOUND)
        tasks_date_sort = tasks.order_by("date")
        next_urgent_due = tasks_date_sort.first().date if tasks_date_sort else None
        data = {
            "todos": tasks.filter(status="toDo").count(),
            "in_progress": tasks.filter(status="inProgress").count(),
            "await_feedback": tasks.filter(status="awaitFeedback").count(),
            "done": tasks.filter(status="done").count(),
            "total": tasks.count(),
            "urgent": tasks.filter(prio="urgent").count(),
            "next_urgent_due": next_urgent_due.strftime("%Y-%m-%d") if next_urgent_due else None,
        }
        return Response(data)
