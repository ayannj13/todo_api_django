from rest_framework import status, viewsets, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Task
from .serializers import TaskSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Task.objects.select_related("user").order_by("-created_at")
        status_param = self.request.query_params.get("status")
        if status_param:
            qs = qs.filter(status=status_param)
        return qs
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="my", url_name="my")
    def my(self, request):
        """
        GET /api/tasks/my/ - only the current user's tasks
        """
        qs = self.get_queryset().filter(user=request.user)
        page = self.paginate_queryset(qs)
        if page is not None:
            ser = self.get_serializer(page, many=True)
            return self.get_paginated_response(ser.data)
        ser = self.get_serializer(qs, many=True)
        return Response(ser.data)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        """
        POST /api/tasks/{id}/complete/ - set status to COMPLETED 
        """
        task = self.get_object()
        task.status = Task.Status.COMPLETED  
        task.save(update_fields=["status", "updated_at"])
        return Response({"detail": "Task marked as completed."}, status=status.HTTP_200_OK)
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]