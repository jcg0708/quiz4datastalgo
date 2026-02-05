from rest_framework import generics, permissions
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer

class IsAdminOrManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrManager] 

    def perform_create(self, serializer):
        start_date = serializer.validated_data.get('start_date')
        today = timezone.now().date()
        
        status = 'CREATED'
        if start_date == today:
            status = 'IN PROGRESS'
            
        serializer.save(status=status)