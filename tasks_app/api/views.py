"""
ViewSets and API views for managing tasks and providing summary statistics.
"""

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from tasks_app.models import Task
from tasks_app.api.serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    """
    API endpoint for listing, creating, retrieving, updating, and deleting tasks.
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SummaryView(ListAPIView):
    """
    API endpoint for retrieving summary statistics about tasks (counts, next urgent due, etc.).
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        """
        Return summary statistics for all tasks. If no tasks exist, return zeros for all fields.
        """
        tasks = self.get_queryset()
        if not tasks.exists():
            data = {
                "todos": 0,
                "in_progress": 0,
                "await_feedback": 0,
                "done": 0,
                "total": 0,
                "urgent": 0,
                "next_urgent_due": None,
            }
            return Response(data, status=status.HTTP_200_OK)
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
