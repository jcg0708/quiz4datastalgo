from rest_framework import viewsets, generics, permissions
from .models import Project, Task
from .serializers import (
    ProjectDetailSerializer, 
    ProjectCreateSerializer, 
    TaskSerializer, 
    TaskCreateSerializer
)
from .permissions import IsAdminOrManager
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit/create objects.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    
    def get_serializer_class(self):
        # Use different serializers for different actions
        if self.action == 'create' or self.action == 'update':
            return ProjectCreateSerializer
        return ProjectDetailSerializer

    def get_permissions(self):
        # "Accessible to the Admin only" for creation
        if self.action == 'create':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]
    
class ProjectTaskCreateView(generics.CreateAPIView):
    """
    API View to create a task specifically for a project.
    Route: POST /api/v1/projects/<project_id>/tasks/
    """
    serializer_class = TaskCreateSerializer
    permission_classes = [IsAdminOrManager] # Only Admin or Manager can access

    def perform_create(self, serializer):
        # Automatically link the new task to the project defined in the URL
        project_id = self.kwargs.get('project_id')
        project = Project.objects.get(pk=project_id)
        serializer.save(project=project)
